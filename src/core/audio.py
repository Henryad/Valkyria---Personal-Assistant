import sounddevice as sd
import numpy as np
import queue


class AudioRecorder:
def __init__(self, samplerate=16000, channels=1, device=None):
self.samplerate = samplerate
self.channels = channels
self.device = device
self.q = queue.Queue()
self._stream = None


def _callback(self, indata, frames, time, status):
if status: print(status)
self.q.put(indata.copy())


def start(self):
self._stream = sd.InputStream(samplerate=self.samplerate, channels=self.channels,
dtype="int16", callback=self._callback, device=self.device)
self._stream.start()


def read_seconds(self, seconds):
n = int(self.samplerate * seconds)
chunks = []
got = 0
while got < n:
data = self.q.get()
chunks.append(data)
got += len(data)
return np.concatenate(chunks, axis=0)


def stop(self):
if self._stream:
self._stream.stop()
self._stream.close()
