import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()


class BrainService:
    def __init__(self, bus):
        self.bus = bus
        # В 2026 году клиент инициализируется так. Он сам найдет GEMINI_API_KEY в .env
        self.client = genai.Client()
        # Используем современную, актуальную модель
        self.model_name = 'gemini-3.5-flash'

    def setup_subscriptions(self):
        self.bus.subscribe("THINK_COMMAND", self.generate_response)

    def generate_response(self, error_context):
        print('[МОЗГ] Генерирую мысль через Gemini 3.5...')

        # Текст от пользователя
        prompt = f"Пользователь словил ошибку: {error_context}. Поддержи его одной короткой смешной фразой."

        try:
            # Новый синтаксис 2026 года:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction="Ты - Archie, саркастичный и умный ИИ-напарник."
                )
            )

            # Достаем текст
            answer = response.text

            # Отправляем в Голос
            self.bus.publish("SPEAK_COMMAND", answer)

        except Exception as e:
            print(f"[МОЗГ] Ошибка API: {e}")