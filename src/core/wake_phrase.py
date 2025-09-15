import numpy as np, sounddevice as sd, re
from core.vad import SimpleVAD
from core.asr_whispercpp import transcribe_whisper_cpp


class WakePhraseDetector:
def __init__(self, sr=16000, device=None, whisper_bin="", model_path="", language="pt", threads=4):
self.sr = sr
self.device = device
self.whisper_bin = whisper_bin
self.model_path = model_path
self.language = language
self.threads = threads
self.vad = SimpleVAD(thresh=0.6, sr=sr)


def listen(self):
with sd.InputStream(samplerate=self.sr, channels=1, dtype="int16", device=self.device):
buf = []
speaking = False
silence = 0
chunk = int(self.sr * 0.2)
while True:
audio = sd.rec(frames=chunk, samplerate=self.sr, channels=1, dtype="int16")
sd.wait()
arr = audio.squeeze()
is_speech = self.vad.is_speech(arr)
buf.append(arr)
if is_speech:
speaking = True; silence = 0
else:
silence += 1
if speaking and silence >= 3:
full = np.concatenate(buf, axis=0)
text = transcribe_whisper_cpp(self.whisper_bin, self.model_path, full, sr=self.sr, language=self.language, threads=self.threads).lower()
buf = []; speaking = False; silence = 0
if re.search(r"\bvalk?yria\b", text) or re.search(r"\bval\b", text):
return "val" if " val " in f" {text} " and "valkyria" not in text else "valkyria"
