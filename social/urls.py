from django.urls import path

from social.views import (
    CheckHookView,
    HookBotView,
    ListSocialsView,
    RunButtonView,
    SetHookView,
)

urlpatterns = [
    path('hook/<int:pk>', HookBotView.as_view(), name='hook'),
    path('check_hook/<int:pk>', CheckHookView.as_view(), name='check_hook'),
    path('set_hook/<int:pk>', SetHookView.as_view(), name='set_hook'),
    path('run_button/<int:pk>', RunButtonView.as_view(), name='run_button'),
    path('<int:pk>', ListSocialsView.as_view(), name='social_list_edit'),
    path('', ListSocialsView.as_view(), name='social_list_or_add'),
]
