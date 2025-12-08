from assistant.pipeline import AssistantPipeline
from assistant.recorder import record
from assistant.tts import speak

assistant = AssistantPipeline()

print("🎤 ZIRA Voice Assistant is LIVE")

while True:
    print("Listening...")
    audio = record(duration=3)

    response = assistant.process_audio(audio)
    print("Assistant:", response)
    speak(response)
