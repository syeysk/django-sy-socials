from django.core.paginator import Paginator
from django.views import View
from django.shortcuts import render
from rest_framework.response import Response

from social.adapters import get_adapter_names
from social.models import Social


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
