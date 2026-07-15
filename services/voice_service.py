import torch
import sounddevice as sd
import queue
import threading


class VoiceService:
    def __init__(self):
        self.speech_queue = queue.Queue()

        # Настройки нейросети
        self.device = torch.device('cpu')

        print("[ГОЛОС] Загрузка нейросети Silero TTS (может занять время)...")
        # Скачиваем/загружаем модель (скачается только 1 раз в кэш)
        self.model, _ = torch.hub.load(
            repo_or_dir='snakers4/silero-models',
            model='silero_tts',
            language='ru',
            speaker='v4_ru',
            verbose = False
        )
        self.model.to(self.device)
        self.sample_rate = 48000
        self.speaker = 'xenia'  # Очень приятный женский голос

        threading.Thread(target=self._worker_loop, daemon=True).start()

    def setup_subscriptions(self, bus):
        self.bus = bus
        bus.subscribe("SPEAK_COMMAND", self.speak)

    def speak(self, text):
        if text.strip():
            self.speech_queue.put(text)

    def _worker_loop(self):
        print("[ГОЛОС] Модуль речи готов!")
        while True:
            text = self.speech_queue.get()
            try:
                # 1. Нейросеть генерирует массив звука
                audio = self.model.apply_tts(
                    text=text,
                    speaker=self.speaker,
                    sample_rate=self.sample_rate

                )

                self.bus.state["is_speaking"] = True
                # 2. Воспроизводим звук через колонки
                sd.play(audio.numpy(), self.sample_rate)
                sd.wait()  # Ждем, пока фраза договорится до конца
                self.bus.state["is_speaking"] = False
            except Exception as e:
                print(f"[ГОЛОС] Ошибка генерации: {e}")