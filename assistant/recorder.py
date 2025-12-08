import sounddevice as sd
import numpy as np
import scipy.signal
import time

TARGET_SR = 16000
DEVICE_INDEX = 1
DEVICE_SR = 44100

def record(duration=3):
    print(f"[MIC] Recording from device {DEVICE_INDEX} for {duration} seconds...")

    audio_buffer = []

    def callback(indata, frames, time_info, status):
        if status:
            print(status)
        audio_buffer.append(indata.copy())

    with sd.InputStream(
        samplerate=DEVICE_SR,
        channels=1,
        dtype='int16',
        device=DEVICE_INDEX,
        callback=callback
    ):
        time.sleep(duration)

    audio = np.concatenate(audio_buffer, axis=0).flatten().astype(np.float32)

    # ✅ Resample 44.1kHz → 16kHz for Vosk
    new_len = int(len(audio) * TARGET_SR / DEVICE_SR)
    audio = scipy.signal.resample(audio, new_len)
    audio = audio.astype(np.int16)

    return audio.tobytes()
