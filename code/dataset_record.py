import numpy as np
from util.audio_buffer import AudioBuffer
from scipy.io import wavfile
import os
from time import sleep

RECORDING_TIME = 10
SAMPLE_RATE = 16000

def main():
    # record audio via AudioBuffer  ## With chunks_per_second = 1 => every chunk corresponds to 1 second
    audio_buffer = AudioBuffer(sample_rate = SAMPLE_RATE, chunks_per_second = 1, chunks = RECORDING_TIME) 
    audio_buffer.start()
    # select file path for data and recordings
    recording_session_name = input("What is this recording session called? ")
    while True:
        record_sample(recording_session_name, audio_buffer)

def record_sample(recording_session: str, buffer: AudioBuffer) -> None:
    input("Start recording by pressing enter ")
    # wait for buffer to fill
    sleep(RECORDING_TIME)
    # fetch recorded data from buffer
    sound_frame = buffer()
    name = input("Name recording sample> ")
    data_path = os.path.join("dataset", "raw", recording_session, "data", name)
    wave_path = os.path.join("dataset", "raw", recording_session, "recordings", name + ".wav")
    # save recording as wav file
    wavfile.write(wave_path, SAMPLE_RATE, sound_frame)
    # save recording as npy array
    np.save(data_path, sound_frame)

if __name__ == "__main__":
    main()
