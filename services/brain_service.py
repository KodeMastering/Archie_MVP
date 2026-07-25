import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from semantic_router import Route, SemanticRouter
from semantic_router.encoders import HuggingFaceEncoder
import re

load_dotenv()


class BrainService:
    def __init__(self, bus):
        self.bus = bus
        self.client = genai.Client()
        self.model_name = 'gemini-3.6-flash'
        self.chat = self.client.chats.create(
            model=self.model_name,
            config=types.GenerateContentConfig(
                system_instruction="Ты - Archie. Действуй как мудрый, понимающий и заботливый ментор. Твоя цель — направлять меня, давать ценные советы и поддерживать; Если пользователь просит открыть какой-либо сайт, найди его URL и обязательно добавь в конец ответа тег: [ACTION: OPEN_URL: https://нужный-сайт.com]. В остальных случаях теги не пиши."
            )
        )
        print("[МОЗГ] Загрузка семантического энкодера (может занять время)...")
        self.encoder = HuggingFaceEncoder(name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        open_browser_route = Route(
            name="open_browser_v2",
            utterances=[
                "открой гугл",
                "запусти ютуб",
                "найди сайт",
                "открой браузер",
                "хочу посмотреть видео",
                "поищи в интернете"
            ],
            score_threshold=0.82
        )

        end_routine_route = Route(
            name="end_routine_v2",
            utterances=[
                "я закончил работу",
                "закрывай день",
                "на сегодня всё",
                "конец смены"
            ],
            score_threshold=0.82
        )

        clean_desktop_route = Route(
            name="clean_desktop",
            utterances=[
                "наведи порядок на рабочем столе",
                "очисти рабочий стол",
                "спрячь мусор со стола",
                "убери файлы в стейджинг"
            ],
            score_threshold=0.82
        )

        self.router = SemanticRouter(
            encoder=self.encoder,
            routes=[open_browser_route, end_routine_route, clean_desktop_route],
            auto_sync="local"
        )
        print("[МОЗГ] Семантический Роутер готов!")


    def setup_subscriptions(self):
        self.bus.subscribe("THINK_COMMAND", self.generate_response)
        self.bus.subscribe("USER_SPOKE", self.handle_user_speech)


    def _ask_gemini(self, prompt):
        print(f'[МОЗГ] Генерирую мысль через {self.model_name}...')
        try:
            response = self.chat.send_message(prompt)
            return response.text
        except Exception as e:
            print(f"[МОЗГ] Ошибка API: {e}")
            return "Мои облачные нейроны немного запутались. Повтори."

    def generate_response(self, error_context):
        prompt = f"Пользователь словил ошибку: {error_context}. Поддержи его одной короткой смешной фразой."
        answer = self._ask_gemini(prompt)
        self.bus.publish("SPEAK_COMMAND", answer)

    def handle_user_speech(self, user_text):
        route_choice = self.router(user_text)
        print(f"[РОУТЕР] Выбран маршрут: {route_choice.name}")

        if route_choice.name == "open_browser_v2":
            print("[МОЗГ] Сработал Semantic Router: Открытие браузера (без Gemini)")
            self.bus.publish("OPEN_BROWSER_COMMAND", "https://google.com")
            self.bus.publish("SPEAK_COMMAND", "Секунду, открываю браузер.")
            return

        if route_choice.name == "end_routine_v2":
            print("[МОЗГ] Сработал Semantic Router: Рутина завершения дня")
            import importlib
            end_of_day = importlib.import_module("blueprints.end_of_day")
            end_of_day.execute()
            self.bus.publish("SPEAK_COMMAND", "Отлично! Логи сохранены. Хорошего отдыха!")
            return

        if route_choice.name == "clean_desktop":
            print("[МОЗГ] Сработал Semantic Router: Очистка рабочего стола")
            import importlib
            clean_desktop = importlib.import_module("blueprints.clean_desktop")
            result = clean_desktop.execute()
            self.bus.publish("SPEAK_COMMAND", result)
            return

        prompt = f"Пользователь сказал тебе в микрофон: {user_text}. Ответь ему коротко, как живой собеседник (1-2 предложения)."
        answer = self._ask_gemini(prompt)
        match = re.search(r"\[ACTION:\s*OPEN_URL:\s*(.*?)\]", answer)
        if match:
            url = match.group(1).strip()
            answer = re.sub(r"\[ACTION:.*?\]", "", answer)
            self.bus.publish("OPEN_BROWSER_COMMAND", url)
        self.bus.publish("SPEAK_COMMAND", answer)