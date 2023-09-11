import json

from django.core.paginator import Paginator
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.views import APIView
from rest_framework import status

from social.adapters import get_adapter_names
from social.models import Social
from social.serializers import SocialSerializer


class ListSocialsView(APIView):
    def get(self, request):
        count_on_page = request.GET.get('count', 10)
        page_number = request.GET.get('p', 1)

        notes = Social.objects.order_by('-pk')
        paginator = Paginator(notes, count_on_page)
        page = paginator.page(page_number)

        auto_schema = AutoSchema()
        serializer_maps = {}
        for subclass_name, subclass in get_adapter_names(True):
            service_serializer = getattr(subclass, 'serializer', None)
            if service_serializer:
                service_map = auto_schema.map_serializer(service_serializer())
                serializer_maps[subclass_name] = []
                for field_name, field_map in service_map['properties'].items():
                    serializer_maps[subclass_name].append({'name': field_name, 'map': field_map})

        context = {
            'socials': [dict(social) for social in page.object_list.values('title', 'credentials', 'adapter', 'pk')],
            'adapters': get_adapter_names(),
            'serializer_maps': serializer_maps,
        }
        for social in context['socials']:
            social['credentials'] = json.loads(social['credentials']) if social['credentials'] else {}

        return render(request, 'social/social_list.html', context)

    def post(self, request, pk=None):
        """The view edits a social or creates a new social if pk=0"""
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if pk:
            instance = Social.objects.get(pk=pk, created_by=request.user)
            if request.user.pk != instance.created_by.pk:
                return Response(status=status.HTTP_403_FORBIDDEN)

            serializer = SocialSerializer(instance, data=request.POST)
            serializer.is_valid(raise_exception=True)
            updated_fields = [
                name for name, value in serializer.validated_data.items() if getattr(instance, name) != value
            ]
            updated_cred_fields = [
                name for name, value in serializer.validated_data['credentials'].items()
                if instance.credentials.get(name) != value
            ]
            serializer.save()
        else:
            serializer = SocialSerializer(data=request.POST)
            serializer.is_valid(raise_exception=True)
            updated_fields = serializer.fields.keys()
            updated_cred_fields = json.loads(serializer.validated_data['credentials']).keys()
            instance = serializer.save(created_by=request.user)

        response_data = {
            'id': instance.pk, 'updated_fields': updated_fields, 'updated_cred_fields': updated_cred_fields,
        }
        return Response(status=status.HTTP_200_OK, data=response_data)

