from assistant.pipeline import AssistantPipeline
from assistant.recorder import record
from assistant.tts import speak
import time

assistant = AssistantPipeline()

print("🎤 ZIRA Voice Assistant is LIVE")

while True:
    print("Listening...")
    audio = record(duration=3)

    # tiny delay so Realtek stops holding the device hostage
    time.sleep(0.2)

    response = assistant.process_audio(audio)
    print("Assistant:", response)
    speak(response)
