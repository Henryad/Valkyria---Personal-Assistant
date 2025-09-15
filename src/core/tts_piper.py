import subprocess


def speak_piper(piper_bin, voice, voice_cfg, text, out_wav="out.wav"):
cmd = [piper_bin, "-m", voice, "-c", voice_cfg, "-f", out_wav]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
p.stdin.write(text.encode("utf-8"))
p.stdin.close()
p.wait()
try:
subprocess.run(["ffplay", "-nodisp", "-autoexit", out_wav], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except Exception:
pass
