from core.event_bus import EventBus

bus = EventBus()

def on_app_opened(data):
    print(f'[ЗРЕНИЕ] Пользователь открыл: {data}')

def on_error(data):
    print(f'[ФРУСТРАЦИЯ] Замечена ошибка: {data}')

bus.subscribe('APP_OPENED', on_app_opened)
bus.subscribe('ERROR_OCCURRED', on_error)
bus.publish("APP_OPENED", "PyCharm")
bus.publish("ERROR_OCCURRED","IndetationError")