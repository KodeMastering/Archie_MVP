class ProactivityEngine:


    def __init__(self, bus):
        self.frustaration_score = 0
        self.bus = bus
        self.current_mission = "FOCUS"
        self.rest_apps = ["Telegram", "YouTube", "Steam", "Discord"]

    def setup_subscriptions(self):
        self.bus.subscribe('ERROR_OCCURRED', self.handle_error)
        self.bus.subscribe("USER_STUCK", self.handle_stuck)
        self.bus.subscribe("APP_OPENED", self.handle_app_changed)
        self.bus.subscribe("USER_SPOKE", self.stop_stress)


    def handle_error(self, error_data):
        if self.current_mission == "REST":
            return
        self.frustaration_score += 20
        # print(f'[ПРОАКТИВНОСТЬ] УРОВЕНЬ СТРЕССА: {self.frustaration_score}/50')
        if self.frustaration_score >= 50:
            self.bus.publish("THINK_COMMAND", error_data)
            self.frustaration_score = 0


    def handle_stuck(self, window_name):
        if self.current_mission == "REST":
            return
        self.frustaration_score += 25
        # print(f'[ПРОАКТИВНОСТЬ] УРОВЕНЬ СТРЕССА: {self.frustaration_score}/50')
        if self.frustaration_score >= 50:
            self.bus.publish("THINK_COMMAND", f"Пользователь уже долго сидит без дела в окне: {window_name}. Спроси, не нужна ли ему помощь, может он залип?")
            self.frustaration_score = 0


    def handle_app_changed(self, window_name):
        is_rest = any(app in window_name for app in self.rest_apps)
        if is_rest:
            self.current_mission = "REST"
        else:
            self.current_mission = "FOCUS"
        print(f"[ПРОАКТИВНОСТЬ] Режим изменен на: {self.current_mission}")

    def stop_stress(self, text):
        if self.frustaration_score > 0:
            self.frustaration_score = 0
            # print("[ПРОАКТИВНОСТЬ] Диалог начат. Стресс сброшен.")