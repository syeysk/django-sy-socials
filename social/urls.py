from django.urls import path

from social.views import (
    ListSocialsView
)

urlpatterns = [
    path('socials/', ListSocialsView.as_view(), name='social_list'),
]
