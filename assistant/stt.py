import os
import tempfile
import subprocess
from faster_whisper import WhisperModel


class SpeechToText:
    def __init__(self):
        # load faster-whisper model
        self.model = WhisperModel("small", device="cpu", compute_type="int8")

        # ffmpeg path (your location)
        self.ffmpeg_path = r"C:\Users\akash\Downloads\ffmpeg-8.0.1-essentials_build\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe"
        os.environ["PATH"] += os.pathsep + os.path.dirname(self.ffmpeg_path)

    def transcribe(self, audio_bytes):
        if not audio_bytes:
            print("Whisper: (empty audio)")
            return ""

        # Save incoming audio as .webm first
        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as f:
            f.write(audio_bytes)
            webm_path = f.name

        # Convert webm → wav
        wav_path = webm_path.replace(".webm", ".wav")

        try:
            subprocess.run(
                [
                    self.ffmpeg_path,
                    "-i", webm_path,
                    "-ac", "1",           # mono
                    "-ar", "16000",       # 16 kHz
                    wav_path,
                    "-y",
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            # Transcribe with faster-whisper
            segments, info = self.model.transcribe(wav_path, language="en")
            text = "".join(seg.text for seg in segments).strip()

            print("Whisper:", text)
            return text

        except Exception as e:
            print("STT Error:", e)
            return ""
