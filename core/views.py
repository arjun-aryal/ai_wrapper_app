import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from .models import ChatSession, ChatMessage
from .serializers import ChatSessionSerializer, ChatMessageSerializer
from .service import get_ai_service


class ChatSessionAPIView(APIView):
    """
    Create new chat sessions and retrieve chat history by session_id.
    """

    def post(self, request):
        """Create a new chat session with a unique UUID."""
        user = request.user if request.user.is_authenticated else None
        session = ChatSession.objects.create(user=user, session_id=str(uuid.uuid4()))
        serializer = ChatSessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, session_id):
        """Retrieve chat history for the given session_id."""
        try:
            session = ChatSession.objects.get(session_id=session_id)
        except ChatSession.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

        messages = session.messages.all().order_by("timestamp")
        serializer = ChatMessageSerializer(messages, many=True)
        return Response({
            "session_id": session.session_id,
            "chat_history": serializer.data
        })


class ChatMessageAPIView(APIView):
    """
    Handle sending user messages and returning AI chatbot responses.
    """

    def post(self, request, session_id):
        # Validate session existence
        try:
            session = ChatSession.objects.get(session_id=session_id)
        except ChatSession.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

        user_message = request.data.get("message", "").strip()
        if not user_message:
            return Response({"error": "Message cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        # Save user message
        user_msg = ChatMessage.objects.create(session=session, sender="user", message=user_message)

        # Update session last_active
        session.last_active = timezone.now()
        session.save()

        # Prepare message history for context if you want to use it
        history = session.messages.all().order_by("timestamp")
        message_history = [{"role": msg.sender, "content": msg.message} for msg in history]

        # Generate AI response
        ai_service = get_ai_service()
        try:
            # Assuming your generate_response method supports a history parameter optionally
            ai_response = ai_service.generate_response(user_message, history=message_history)
        except Exception as e:
            return Response({"error": f"AI service error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Save bot response
        bot_msg = ChatMessage.objects.create(session=session, sender="bot", message=ai_response.content)

        return Response({
            "user_message": user_msg.message,
            "bot_response": bot_msg.message,
            "model_used": ai_response.model_name,
            "response_time_ms": ai_response.response_time_ms
        }, status=status.HTTP_200_OK)
