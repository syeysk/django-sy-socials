from django.urls import path

from message.views import (
    MessageView
)

urlpatterns = [
    path('send/', MessageView.as_view(), name='send_message'),
]
