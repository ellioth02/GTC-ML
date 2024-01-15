import numpy as np
from util.audio_buffer import AudioBuffer
from scipy.io import wavfile
import os
from time import sleep

__FILE_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(__FILE_PATH, "..")
DATA_PATH = os.path.join(ROOT_PATH, "dataset", "raw")

RECORDING_TIME = 10
SAMPLE_RATE = 16000

def main():
    # record audio via AudioBuffer  ## With chunks_per_second = 1 => every chunk corresponds to 1 second
    audio_buffer = AudioBuffer(sample_rate = SAMPLE_RATE, chunks_per_second = 1, chunks = RECORDING_TIME) 
    audio_buffer.start()
    # select file path for data and recordings
    recording_session_name = input("What is this recording session called? ")
    # create recording directories
    session_path = os.path.join(DATA_PATH, recording_session_name)
    create_directory(os.path.join(session_path, "data"))
    create_directory(os.path.join(session_path, "recordings"))
    # start recording
    while True:
        record_sample(recording_session_name, audio_buffer)

def record_sample(recording_session: str, buffer: AudioBuffer) -> None:
    input("Start recording by pressing enter ")
    # wait for buffer to fill
    sleep(RECORDING_TIME)
    # fetch recorded data from buffer
    sound_frame = buffer()
    name = input("Name recording sample> ")
    data_path = os.path.join(DATA_PATH, recording_session, "data", name)
    wave_path = os.path.join(DATA_PATH, recording_session, "recordings", name + ".wav")
    # save recording as wav file
    wavfile.write(wave_path, SAMPLE_RATE, sound_frame)
    # save recording as npy array
    np.save(data_path, sound_frame)

# create directory if it does not exist
def create_directory(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)

if __name__ == "__main__":
    main()
