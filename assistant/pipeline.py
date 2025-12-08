from assistant.stt import SpeechToText
from assistant.tts import speak
from assistant.connectivity import is_online
from assistant.offline_engine import OfflineEngine
from assistant.intents import get_intent


class AssistantPipeline:
    def __init__(self):
        self.offline_engine = OfflineEngine()

    # ✅ REAL AUDIO MODE
    def process_audio(self, audio_bytes):
        online = is_online()

        stt = SpeechToText(mode="online" if online else "offline")
        text = stt.transcribe(audio_bytes)

        return self._process_text_logic(text)

    # ✅ REAL TEXT MODE (NO STT)
    def process_text(self, text):
        return self._process_text_logic(text)

    # ✅ SHARED LOGIC
    def _process_text_logic(self, text):
        if not text or not text.strip():
            return "I could not hear anything."

        intent = get_intent(text)

        if intent == "query":
            return self.offline_engine.query(text)

        return "I don't know how to answer that yet."
