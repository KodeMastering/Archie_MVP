import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()


class BrainService:
    def __init__(self, bus):
        self.bus = bus
        self.client = genai.Client()
        self.model_name = 'gemini-3.1-flash-lite'

    def setup_subscriptions(self):
        self.bus.subscribe("THINK_COMMAND", self.generate_response)
        self.bus.subscribe("USER_SPOKE", self.handle_user_speech)


    def _ask_gemini(self, prompt):
        print(f'[МОЗГ] Генерирую мысль через {self.model_name}...')
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents= prompt,
                config=types.GenerateContentConfig(
                    system_instruction="Ты - Archie. Действуй как мудрый, понимающий и заботливый ментор. Твоя цель — направлять меня, давать ценные советы и поддерживать; Если пользователь просит открыть гугл, браузер или поискать информацию, ты должен добавить в конец своего ответа специальный тег: [ACTION: OPEN_GOOGLE]. В остальных случаях теги не пиши."
                )
            )
            return response.text
        except Exception as e:
            print(f"[МОЗГ] Ошибка API: {e}")
            return "Мои облачные нейроны немного запутались. Повтори."

    def generate_response(self, error_context):
        prompt = f"Пользователь словил ошибку: {error_context}. Поддержи его одной короткой смешной фразой."
        answer = self._ask_gemini(prompt)
        self.bus.publish("SPEAK_COMMAND", answer)

    def handle_user_speech(self, user_text):
        prompt = f"Пользователь сказал тебе в микрофон: {user_text}. Ответь ему коротко, как живой собеседник (1-2 предложения)."
        answer = self._ask_gemini(prompt)
        print(f"Gemini say: {answer}")
        if "[ACTION: OPEN_GOOGLE]" in answer:
            answer = answer.replace("[ACTION: OPEN_GOOGLE]", "")
            self.bus.publish("OPEN_BROWSER_COMMAND", None)
        self.bus.publish("SPEAK_COMMAND", answer)