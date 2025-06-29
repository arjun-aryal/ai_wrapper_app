from rest_framework import serializers
from .models import ChatMessage, ChatSession

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'


class ChatSessionSerializer(serializers.ModelSerializer):
    message = ChatMessageSerializer(many=True,read_only=True)

    class Meta:
        model = ChatSession
        fields = '__all__'




# class ChatRequestSerializer(serializers.Serializer):
#     session_id = serializers.CharField()
#     message = serializers.CharField()
#     provider = serializers.ChoiceField(choices=[('openai', 'OpenAI'), ('gemini', 'Gemini')], required=False)