from core.event_bus import EventBus
from services.voice_service import VoiceService
from services.proactivity_engine import ProactivityEngine
from services.brain_service import BrainService

bus = EventBus()
voice = VoiceService()
voice.setup_subscriptions(bus)
Brain = BrainService(bus)
Brain.setup_subscriptions()
Proactivity = ProactivityEngine(bus)
Proactivity.setup_subscriptions()


def on_app_opened(data):
    print(f'[ЗРЕНИЕ] Пользователь открыл: {data}')

def on_error(data):
    print(f'[ФРУСТРАЦИЯ] Замечена ошибка: {data}')

bus.subscribe('APP_OPENED', on_app_opened)
bus.subscribe('ERROR_OCCURRED', on_error)
bus.publish("APP_OPENED", "PyCharm")
bus.publish("ERROR_OCCURRED","IndetationError")
bus.publish('ERROR_OCCURRED', 'SyntaxError: invalid syntax')
bus.publish('ERROR_OCCURRED', 'ModuleNotFoundError: no module named django')
bus.publish("SPEAK_COMMAND", 'ABCDEFGH')

