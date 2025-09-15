import subprocess, tempfile, os, wave, numpy as np


def write_wav(path, audio_np, sr=16000):
with wave.open(path, "wb") as f:
f.setnchannels(1)
f.setsampwidth(2)
f.setframerate(sr)
f.writeframes(audio_np.astype("int16").tobytes())


def transcribe_whisper_cpp(whisper_bin, model_path, audio_np, sr=16000, language="pt", threads=6):
with tempfile.TemporaryDirectory() as td:
wav = os.path.join(td, "in.wav")
write_wav(wav, audio_np, sr)
cmd = [
whisper_bin, "-m", model_path, "-f", wav,
"-l", language, "-np", "-nt", "-of", os.path.join(td, "out"),
"-t", str(threads)
]
subprocess.run(cmd, check=True, capture_output=True)
with open(os.path.join(td, "out.txt"), "r", encoding="utf-8") as fh:
text = fh.read().strip()
return text
