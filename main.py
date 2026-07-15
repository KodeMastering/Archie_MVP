import time
from core.event_bus import EventBus
from services.voice_service import VoiceService
from services.proactivity_engine import ProactivityEngine
from services.brain_service import BrainService
from services.vision_service import VisionService
from services.Hearing_service import HearingService
from services.action_service import ActionService

bus = EventBus()
voice = VoiceService()
voice.setup_subscriptions(bus)
Brain = BrainService(bus)
Brain.setup_subscriptions()
Proactivity = ProactivityEngine(bus)
Proactivity.setup_subscriptions()
Vision = VisionService(bus)
Hearing = HearingService(bus)
Action = ActionService(bus)
Action.setup_subscriptions()


def on_app_opened(data):
    print(f'[ЗРЕНИЕ] Пользователь открыл: {data}')

def on_error(data):
    print(f'[ФРУСТРАЦИЯ] Замечена ошибка: {data}')

bus.subscribe('APP_OPENED', on_app_opened)
bus.subscribe('ERROR_OCCURRED', on_error)
Vision.start_scanning()
Hearing.start_listening()

while True:
    time.sleep(1)