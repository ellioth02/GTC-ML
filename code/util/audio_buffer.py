import pyaudio
import numpy as np
from collections import deque
import threading
from time import sleep


class AudioBuffer:
    
    def __init__(self, sample_rate: int = 8000, chunks_per_second: int = 10, chunks: int = 5) -> None:
        self.ready = False
        self.rate = sample_rate
        self.chunk_size = int(self.rate / chunks_per_second)
        self.chunks = chunks
        self.stream = pyaudio.PyAudio().open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            )
        self.thread = threading.Thread(target=self._collect_data, daemon=True)
        self.frames = deque(maxlen=self.chunks)

    def get_new_data(self):
        while not self.ready:
            continue
        self.ready = False
        return self.get_data()

    def get_data(self):
        return np.concatenate(self.frames)

    def __call__(self):
        return self.get_new_data()
    
    def __len__(self):
        return self.chunk_size * self.chunks
    
    def is_full(self):
        return len(self.frames) == self.chunks
    
    def start(self):
        self.thread.start()
        while not self.is_full(): # wait until the buffer is filled
            sleep(0.1)
        
    def _collect_data(self):
        while True:
            raw_data = self.stream.read(self.chunk_size) # wait for a new chunk
            decoded = np.frombuffer(raw_data, np.int16)
            self.frames.append(decoded) # add chunk to buffer
            self.ready = True # signal new chunk



if __name__ == "__main__":
    audio_buffer = AudioBuffer()
    audio_buffer.start()
    print(audio_buffer().shape)
