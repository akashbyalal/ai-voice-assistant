from assistant.stt import SpeechToText
from assistant.offline_engine import OfflineEngine
from assistant.intents import get_intent
from assistant.connectivity import internet_available

import httpx
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("ONLINE_API_URL")
API_KEY = os.getenv("ONLINE_API_KEY")


class AssistantPipeline:

    # ---------------------------
    # ONLINE MODEL CALL
    # ---------------------------
    async def ask_online_model(self, query: str):
        if not API_URL:
            return None

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "openai/gpt-4o-mini",
            "messages": [{"role": "user", "content": query}],
        }

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.post(API_URL, json=payload, headers=headers)
                r.raise_for_status()
                data = r.json()
                return data["choices"][0]["message"]["content"]
        except Exception:
            return None

    # ---------------------------
    # SETUP
    # ---------------------------
    def __init__(self):
        self.offline_engine = OfflineEngine()
        self.stt = SpeechToText()

    # ---------------------------
    # AUDIO PROCESSING
    # ---------------------------
    def process_audio(self, audio_bytes, mode="online"):
        text = self.stt.transcribe(audio_bytes)
        return text, self._process_text_logic(text, mode)

    # ---------------------------
    # TEXT PROCESSING
    # ---------------------------
    def process_text(self, text, mode="online"):
        return text, self._process_text_logic(text, mode)

    # ---------------------------
    # MAIN LOGIC
    # ---------------------------
    async def _process_text_logic(self, text, mode):
        if not text or not text.strip():
            return "I could not hear anything."

        intent = get_intent(text)

        if intent == "query":

            # TRY ONLINE
            if mode in ("online", "hybrid") and internet_available():
                online_answer = await self.ask_online_model(text)
                if online_answer:
                    return f"[Online] {online_answer}"

            # FALLBACK OFFLINE
            if mode in ("offline", "hybrid"):
                offline_answer = self.offline_engine.query(text)
                if offline_answer:
                    return f"[Offline] {offline_answer}"

            return "I could not find an answer online or offline."

        return "I don't know how to answer that yet."

    # ---------------------------
    # STREAMING ENDPOINT SUPPORT (dummy streaming)
    # ---------------------------
    async def ask_online_stream(self, text, mode):
        answer = await self.ask_online_model(text)
        if not answer:
            yield "[No online answer]"
        else:
            for token in answer.split():
                yield token + " "
