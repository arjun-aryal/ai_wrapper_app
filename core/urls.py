from django.urls import path
from .views import ChatSessionAPIView, ChatMessageAPIView

urlpatterns = [
    path('sessions/', ChatSessionAPIView.as_view(), name='chat-session-create'),
    path('sessions/<str:session_id>/', ChatSessionAPIView.as_view(), name='chat-session-detail'),
    path('sessions/<str:session_id>/messages/', ChatMessageAPIView.as_view(), name='chat-message-send'),
]
