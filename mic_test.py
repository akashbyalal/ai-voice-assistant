import sounddevice as sd
import numpy as np

DEVICE_INDEX = 1   # Microphone Array (Realtek)
SR = 44100

print("Speak loudly for 3 seconds...")
audio = sd.rec(int(3 * SR), samplerate=SR, channels=1, dtype='int16', device=DEVICE_INDEX)
sd.wait()

print("Peak value:", np.max(np.abs(audio)))
