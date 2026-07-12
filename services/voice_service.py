import pyttsx3

class VoiceService:


    def __init__(self):
        self.engine = pyttsx3.init()


    def speak(self, text: str):
        self.engine.say(text)
        self.engine.runAndWait()

    def setup_subscriptions(self, bus):
        bus.subscribe("SPEAK_COMMAND", self.speak)
