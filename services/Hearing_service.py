import threading
import speech_recognition as sr

class HearingService:

    def __init__(self, bus):
        self.bus = bus


    def start_listening(self):
        thread = threading.Thread(target=self._listen_loop(), daemon=True)
        thread.start()
        print("[СЛУХ] Модуль ушей активирован.")

    def _listen_loop(self):
        while True:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                print("[СЛУХ] Слушаю микрофон...")
                audio = recognizer.listen(source)

                try:
                    text = recognizer.recognize_google(audio, language="ru-RU")
                    if text.strip():  # Если текст не пустой
                        print(f"[СЛУХ] Пользователь сказал: {text}")
                        self.bus.publish("USER_SPOKE", text)

                except sr.UnknownValueError:
                    pass