from django.db import models
from django.contrib.auth.models import User


class ChatSession(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    session_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Session {self.session_id} ({self.user.username if self.user else 'Guest'})"
    

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=10, choices=[('user', 'User'), ('bot', 'Bot')])
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.sender} ({self.timestamp}): {self.message[:50]}"


class AIInteraction(models.Model):
    chat_message = models.OneToOneField(ChatMessage, on_delete=models.CASCADE)
    ai_model_used = models.CharField(max_length=50)  # Store AI model name
    confidence_score = models.FloatField(null=True, blank=True)  # AI response confidence
    response_time_ms = models.IntegerField(null=True, blank=True)  # AI response time

    def __str__(self):
        return f"AI Response for {self.chat_message.id} - {self.ai_model_used}"