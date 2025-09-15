import yaml, numpy as np, sys
from core.tts_piper import speak_piper
from core.llm_llamacpp import LocalLLM
from core.router import route_decision
from core.tools import spec_for_llm
from core.asr_whispercpp import transcribe_whisper_cpp
from core.audio import AudioRecorder
from core.wake_phrase import WakePhraseDetector
from core.vad import SimpleVAD


def capture_utterance(cfg):
rec = AudioRecorder(samplerate=cfg["audio"]["sample_rate"], device=cfg["audio"]["device"])
vad = SimpleVAD(thresh=cfg["audio"]["vad_threshold"], sr=cfg["audio"]["sample_rate"])
rec.start()
print("Fale seu comando…")
buf = []; silence_count = 0
while True:
chunk = rec.read_seconds(0.2)
buf.append(chunk)
speaking = vad.is_speech(chunk)
if speaking: silence_count = 0
else: silence_count += 1
if silence_count > 5 or len(buf)*0.2 > cfg["audio"]["max_utterance_sec"]:
break
rec.stop()
audio = np.concatenate(buf, axis=0).squeeze()
return audio


def main():
cfg = yaml.safe_load(open("config.yaml","r",encoding="utf-8"))


llm = LocalLLM(model_path=cfg["llm"]["model_path"],
n_ctx=cfg["llm"]["n_ctx"],
n_threads=cfg["llm"]["n_threads"],
temperature=cfg["llm"]["temperature"])


print("Valkyria pronta. Diga 'Val' ou 'Valkyria' para ativar.")
ph = cfg["wake"]["phrase"]
ww = WakePhraseDetector(sr=cfg["audio"]["sample_rate"], device=cfg["audio"]["device"],
whisper_bin=ph["whisper_bin"], model_path=ph["model_path"],
language="pt", threads=ph["threads"])


while True:
hot = ww.listen()
print(f"Wake detectado: {hot}.")
speak_piper(cfg["tts"]["piper_bin"], cfg["tts"]["voice"], cfg["tts"]["voice_config"],
"Oi, em que posso ajudar?", cfg["tts"]["output_wav"])


audio = capture_utterance(cfg)
text = transcribe_whisper_cpp(cfg["asr"]["whisper_bin"], cfg["asr"]["model_path"], audio,
sr=cfg["audio"]["sample_rate"], language=cfg["asr"]["language"],
threads=cfg["asr"]["threads"])
print("Você disse:", text)


decision = llm.decide(text, spec_for_llm())
reply = route_decision(decision)
print("Valkyria:", reply)


speak_piper(cfg["tts"]["piper_bin"], cfg["tts"]["voice"], cfg["tts"]["voice_config"],
reply, cfg["tts"]["output_wav"])


if __name__ == "__main__":
try:
main()
except KeyboardInterrupt:
sys.exit(0)
