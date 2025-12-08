from faster_whisper import WhisperModel
import numpy as np
import tempfile
import scipy.io.wavfile as wavfile
import os
import subprocess


class SpeechToText:
    def __init__(self, mode="offline"):
        # Small model = good balance of speed + accuracy
        self.model = WhisperModel("small", device="cpu", compute_type="int8")

        # ✅ Hard-link ffmpeg.exe since it's NOT in PATH
        self.ffmpeg_path = r"C:\Users\akash\Downloads\ffmpeg-8.0.1-essentials_build\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe"

        os.environ["PATH"] += os.pathsep + os.path.dirname(self.ffmpeg_path)

    def transcribe(self, audio_bytes):
        audio_np = np.frombuffer(audio_bytes, dtype=np.int16)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            wavfile.write(f.name, 16000, audio_np)

            segments, info = self.model.transcribe(f.name, language="en")


        text = ""
        for seg in segments:
            text += seg.text + " "

        text = text.strip()

        print("🎧 WHISPER OUTPUT:", text)

        return text
