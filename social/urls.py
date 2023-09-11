from django.urls import path

from social.views import (
    ListSocialsView
)

urlpatterns = [
    path('<int:pk>', ListSocialsView.as_view(), name='social_list_edit'),
    path('', ListSocialsView.as_view(), name='social_list_or_add'),
]
