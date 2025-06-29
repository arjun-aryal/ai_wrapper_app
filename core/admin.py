from django.contrib import admin
from .models import ChatMessage, ChatSession, AIInteraction
# Register your models here.

admin.site.register(ChatMessage)
admin.site.register(ChatSession)
admin.site.register(AIInteraction)