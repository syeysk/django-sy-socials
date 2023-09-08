from django.core.paginator import Paginator
from django.views import View
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status

from social.adapters import get_adapter_names
from social.models import Social
from social.serializers import SocialSerializer


class ListSocialsView(View):
    def get(self, request):
        count_on_page = request.GET.get('count', 10)
        page_number = request.GET.get('p', 1)

        notes = Social.objects.order_by('-pk')
        paginator = Paginator(notes, count_on_page)
        page = paginator.page(page_number)
        tests = [
            {'title': 'title 1', 'adapter': 'Telegram', 'id': 1},
            {'title': 'title 2', 'adapter': 'Telegram', 'id': 2},
            {'title': 'title 3', 'adapter': 'Discord', 'id': 3},
            {'title': 'title 4', 'adapter': 'Telegram', 'id': 4},
        ]
        context = {
            'socials': tests,  # [dict(social) for social in page.object_list.values()],
            'adapters': get_adapter_names(),
        }
        return render(request, 'social/social_list.html', context)

    def post(self, request, pk=None):
        """The view edits a social or creates a new social if pk=0"""
        # if not request.user.is_authenticated:
        #     return Response(status=status.HTTP_401_UNAUTHORIZED)

        if pk:
            instance = Social.objects.get(pk=pk, user=request.user)
            if request.user.pk != instance.user.pk:
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
            updated_cred_fields = serializer.validated_data['credentials'].keys()
            instance = serializer.save(user=request.user)

        response_data = {
            'id': instance.pk, 'updated_fields': updated_fields, 'updated_cred_fields': updated_cred_fields,
        }
        return Response(status=status.HTTP_200_OK, data=response_data)

