from django.urls import path

from social.views import (
    HookBotView,
    ListSocialsView,
)

urlpatterns = [
    path('hook/<int:pk>', HookBotView.as_view(), name='hook'),
    path('<int:pk>', ListSocialsView.as_view(), name='social_list_edit'),
    path('', ListSocialsView.as_view(), name='social_list_or_add'),
]
