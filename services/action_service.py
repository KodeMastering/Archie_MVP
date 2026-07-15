import webbrowser

class ActionService:

    def __init__(self, bus):
        self.bus = bus

    def setup_subscriptions(self):
        self.bus.subscribe("OPEN_BROWSER_COMMAND", self.actions)


    def actions(self, command):
        webbrowser.open(command)
        print(f"[ДЕЙСТВИЕ] Открываю: {command}")