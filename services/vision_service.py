import uiautomation as auto
import threading
import time


class VisionService:
    def __init__(self, bus):
        self.bus = bus
        self.last_window = ""
        self.window_start_time = time.time()

    def start_scanning(self):
        thread = threading.Thread(target=self._scan_loop, daemon=True)
        thread.start()
        print("[ЗРЕНИЕ] Модуль Z-Sense активирован. Сканирую окна...")

    def _scan_loop(self):
        while True:
            try:
                window = auto.GetForegroundControl()

                if window:
                    current_window = window.Name

                    if current_window and current_window != self.last_window:
                        self.last_window = current_window
                        self.bus.publish("APP_OPENED", current_window)
                        self.window_start_time = time.time()
                    else:
                        self.window_pass_time = time.time() - self.window_start_time
                        if self.window_pass_time >= 10:
                            self.bus.publish("USER_STUCK", current_window)
                            self.window_start_time = time.time()
            except Exception as e:
                print(f"[ЗРЕНИЕ] Скрытая ошибка: {e}")

            time.sleep(3)