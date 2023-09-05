from django.core.paginator import Paginator
from django.views import View
from django.shortcuts import render
from rest_framework.response import Response

from social.models import Social


class ListSocialsView(View):
    def get(self, request):
        count_on_page = request.GET.get('count', 10)
        page_number = request.GET.get('p', 1)

        notes = Social.objects.order_by('-pk')
        paginator = Paginator(notes, count_on_page)
        page = paginator.page(page_number)
        context = {
            'page': page,
        }
        return render(request, 'social/social_list.html', context)
