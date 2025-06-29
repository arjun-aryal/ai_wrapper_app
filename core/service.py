import time
import openai
import os
import requests
import google.generativeai as genai
class AIService():
    def generate_response(self,prompt):
        pass

class AIResponse:
    def __init__(self, content, model_name, confidence=None, response_time_ms=None):
        self.content = content
        self.model_name = model_name
        self.confidence = confidence
        self.response_time_ms = response_time_ms


class OpenAIService(AIService):
    def generate_response(self, prompt,history=None):

        start_time = time.time()
        OPENAI_API_KEY ="some_value"
        openai.api_key = OPENAI_API_KEY

# https://platform.openai.com/docs/api-reference/chat/create?lang=python
        messages = history if history else [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages =messages
            # messages=[{"role": "user", "content": prompt}]
        )
        # return response["choices"][0]["message"]["content"]
        duration = int((time.time() - start_time) * 1000)
        return AIResponse(content=response["choices"][0]["message"]["content"], model_name="gpt-4", response_time_ms=duration)
    

class ClaudeService:
    def generate_response(self, prompt):
        start_time = time.time()
        ANTHROPIC_API_KEY = os.getenv("CLAUDE_API_KEY")
        CLAUDE_URL = "https://api.anthropic.com/v1/complete"
        
        headers = {
            "x-api-key": ANTHROPIC_API_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "model": "claude-2",
            "prompt": prompt,
            "max_tokens_to_sample": 200
        }
        response = requests.post(CLAUDE_URL, headers=headers, json=data)
        # return response.json()["completion"]
        duration = int((time.time() - start_time) * 1000)
        return AIResponse(content=response.json().get("completion", ""), model_name="claude-2", response_time_ms=duration)


class GeminiService(AIService):
    def generate_response(self, prompt):
        start_time = time.time()
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        # return response.text 
        # start_time = time.time()
        duration = int((time.time() - start_time) * 1000)
        return AIResponse(content=response.text, model_name="gemini-pro", response_time_ms=duration)

    
def get_ai_service():
    ai_provider = os.getenv("AI_PROVIDER", "openai").lower()
    
    if ai_provider == "gemini":
        return GeminiService()
    elif ai_provider == "claude":
        return ClaudeService()
    elif ai_provider == "openai":
        return OpenAIService()
    else:
        raise ValueError(f"Unknown AI provider: {ai_provider}")