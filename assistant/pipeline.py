from assistant.stt import SpeechToText
from assistant.offline_engine import OfflineEngine
from assistant.intents import get_intent

class AssistantPipeline:
    def __init__(self):
        self.offline_engine = OfflineEngine()
        self.stt = SpeechToText()   # always whisper

    def process_audio(self, audio_bytes):
        text = self.stt.transcribe(audio_bytes)
        return self._process_text_logic(text)

    def process_text(self, text):
        return self._process_text_logic(text)

    def _process_text_logic(self, text):
        if not text or not text.strip():
            return "I could not hear anything."

        intent = get_intent(text)

        if intent == "query":
            return self.offline_engine.query(text)

        return "I don't know how to answer that yet."
