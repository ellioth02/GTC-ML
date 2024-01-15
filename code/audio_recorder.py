from typing import Any
import tensorflow as tf
import tensorflow_io as tfio 
from util.audio_buffer import AudioBuffer
from scipy.io import wavfile

# wrapper class for audio buffer with added tensorflow functionality
class Recorder:
    # constructor
    def __init__(self) -> None:
        # create audio recording buffer
        sample_rate = 16_000
        self.audio_buffer = AudioBuffer(sample_rate = sample_rate, chunks_per_second = 1/5, chunks = 1)
    
    def __call__(self):
        return self.get_audio()
    
    # start recording
    def start(self):
        self.audio_buffer.start()

    # returns 5s of audio as tf.tensor
    def get_audio(self):
        data = self.audio_buffer()
        wavfile.write("./tmp.wav", self.audio_buffer.rate, data)
        waveform = self.__load_wav_16k_mono("./tmp.wav")
        return waveform

    # Utility functions for loading audio files and making sure the sample rate is correct.
    def __load_wav_16k_mono(self, filename):
        """ Load a WAV file, convert it to a float tensor, resample to 16 kHz single-channel audio. """
        file_contents = tf.io.read_file(filename)
        wav, sample_rate = tf.audio.decode_wav(
            file_contents,
            desired_channels=1)
        wav = tf.squeeze(wav, axis=-1)
        sample_rate = tf.cast(sample_rate, dtype=tf.int64)
        wav = tfio.audio.resample(wav, rate_in=sample_rate, rate_out=16000)
        return wav
