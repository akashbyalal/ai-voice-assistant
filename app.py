import asyncio
import time

from assistant.pipeline import AssistantPipeline
from assistant.recorder import record
from assistant.tts import speak


assistant = AssistantPipeline()

print("🎤 ZIRA Voice Assistant is LIVE")


async def main_loop():
    while True:
        print("Listening...")
        audio = record(duration=3)

        # small delay to release the mic
        time.sleep(0.2)

        # process audio → (text, answer)
        text, answer = assistant.process_audio(audio)

        # answer from pipeline is async, so we await it
        answer = await answer  

        print(f"User said: {text}")
        print(f"Assistant: {answer}")

        speak(answer)


# run async loop
asyncio.run(main_loop())
