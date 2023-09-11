from django.urls import path

from social.views import (
    ListSocialsView
)

urlpatterns = [
    path('socials/', ListSocialsView.as_view(), name='social_list_or_add'),
    path('socials/<int:pk>', ListSocialsView.as_view(), name='social_list_edit'),
]
