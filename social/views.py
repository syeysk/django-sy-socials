import json

from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, resolve_url
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.views import APIView
from rest_framework import status

from social.adapters import get_adapter_names, get_adapters_properties
from social.bots import bot_name_to_class, get_bot_names
from social.models import Social
from social.serializers import SocialSerializer


class ListSocialsView(APIView):
    def get(self, request):
        count_on_page = request.GET.get('count', 10)
        page_number = request.GET.get('p', 1)

        socials = Social.objects.order_by('-pk')
        if request.user.is_authenticated:
            socials = socials.filter(created_by=request.user)

        paginator = Paginator(socials, count_on_page)
        page = paginator.page(page_number)

        auto_schema = AutoSchema()
        adapter_maps = {}
        bots_by_adapter = {}
        bot_maps_by_adapter = {}
        for adapter_name, adapter_class in get_adapter_names(True):
            adapter_serializer = getattr(adapter_class, 'serializer', None)
            if adapter_serializer:
                adapter_map = auto_schema.map_serializer(adapter_serializer())
                adapter_maps[adapter_name] = adapter_map['properties']

            bot_maps_by_adapter[adapter_name] = {}
            bots_by_adapter[adapter_name] = get_bot_names(adapter_name)
            for bot_name, bot_class in get_bot_names(adapter_name, True):
                bot_serializer = getattr(bot_class, 'serializer', None)
                if bot_serializer:
                    bot_map = auto_schema.map_serializer(bot_serializer())
                    bot_maps_by_adapter[adapter_name][bot_name] = bot_map['properties']

        fields = ['credentials', 'bot_settings', 'pk'] if request.user.is_authenticated else []
        socials = [
            dict(social) for social in page.object_list.values('title', 'adapter', 'bot', *fields)
        ]
        context = {
            'socials': socials,
            'adapters': get_adapters_properties(),
            'serializer_maps': adapter_maps,
            'bots_by_adapter': bots_by_adapter,
            'bot_maps_by_adapter': bot_maps_by_adapter,
        }
        if 'credentials' in fields:
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
                name for name, value in json.loads(serializer.validated_data['credentials']).items()
                if json.loads(instance.credentials).get(name) != value
            ]
            updated_bot_settings_fields = [
                name for name, value in serializer.validated_data['bot_settings'].items()
                if instance.bot_settings.get(name) != value
            ]
            serializer.save()
        else:
            serializer = SocialSerializer(data=request.POST)
            serializer.is_valid(raise_exception=True)
            updated_fields = serializer.fields.keys()
            updated_cred_fields = json.loads(serializer.validated_data['credentials']).keys()
            updated_bot_settings_fields = serializer.validated_data['bot_settings'].keys()
            instance = serializer.save(created_by=request.user)

        response_data = {
            'id': instance.pk,
            'updated_fields': updated_fields,
            'updated_cred_fields': updated_cred_fields,
            'updated_bot_settings_fields': updated_bot_settings_fields,
        }
        return Response(status=status.HTTP_200_OK, data=response_data)


class HookBotView(APIView):
    def post(self, request, pk):
        social = Social.objects.get(pk=pk)
        bot_class = bot_name_to_class(social.adapter, social.bot)
        credentials = json.loads(social.credentials)
        bot = bot_class(social, **credentials)
        if hasattr(bot, 'verify_hook'):
            if not bot.verify_hook(request):
                return Response(status=status.HTTP_403_FORBIDDEN)

        return bot.hook_post_view(request)


class CheckHookView(APIView):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        social = Social.objects.get(pk=pk, created_by=request.user)
        bot_class = bot_name_to_class(social.adapter, social.bot)
        credentials = json.loads(social.credentials)
        bot = bot_class(social, **credentials)
        return Response(status=status.HTTP_200_OK, data={'hook_url': bot.get_hook()})


class SetHookView(APIView):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        social = Social.objects.get(pk=pk, created_by=request.user)
        bot_class = bot_name_to_class(social.adapter, social.bot)
        credentials = json.loads(social.credentials)
        bot = bot_class(social, **credentials)
        hook_url = '{}{}'.format(settings.SITE_URL, resolve_url('hook', pk=pk))
        return Response(status=status.HTTP_200_OK, data={'ok': bot.set_hook(hook_url)})
