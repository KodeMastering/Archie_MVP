class ProactivityEngine:


    def __init__(self, bus):
        self.frustaration_score = 0
        self.bus = bus

    def setup_subscriptions(self):
        self.bus.subscribe('ERROR_OCCURRED', self.handle_error)


    def handle_error(self, error_data):
        self.frustaration_score += 20
        print(f'[ПРОАКТИВНОСТЬ] УРОВЕНЬ СТРЕССА: {self.frustaration_score}/50')
        if self.frustaration_score >= 50:
            self.bus.publish("THINK_COMMAND", error_data)
            self.frustaration_score = 0