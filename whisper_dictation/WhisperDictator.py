import pyaudio
import wave
import numpy as np
import threading
import shlex
import os
from ctypes import *
from contextlib import contextmanager

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int,
                               c_char_p)


def py_error_handler(filename, line, function, err, fmt):
    pass


c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)


@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)


class Transcriber(object):
    """A class to transcribe the audio.
    """

    def __init__(self, model) -> None:
        self.model = model

    def transcribe(self, audio_data: np.ndarray, language: str = "en") -> str:
        """Transcribe the audio data.
        """
        result = self.model.transcribe(
            audio_data, language=language, fp16=False)

        result_text = result['text']
        escaped_result_text = shlex.quote(result_text)
        os.system(f'kdialog --title "Dictation copied" --passivepopup {escaped_result_text}')

        # os.system(f"wl-copy '{result['text']}")

        # copy to wl-copy, not using f-string
        os.system("wl-copy " + result['text'])

        return result["text"]


class WhisperDictator(object):
    """An audio object to record the microphone.
    """

    def __init__(
        self,
        transcriber,
        save_audio: bool = False,
    ) -> None:
        self.recording = False

        self.transcriber = transcriber

        self.save_audio = save_audio

    # the start function implement the function to start recording
    def start(self, language: str = None) -> None:
        # start a new thread to record the audio

        # setup a timer, if the recording is not stopped after 300 seconds, stop it
        timer = threading.Timer(300, self.stop)
        timer.start()

        thread = threading.Thread(target=self._record, args=(language, ))
        thread.start()

    # the stop function implement the function to stop recording
    def stop(self) -> None:
        self.recording = False

    # the record function implement the function to record
    def _record(self, language: str) -> None:

        self.recording = True
        # audio parameters
        chunk = 1024
        sample_format = pyaudio.paInt16
        channels = 1
        rate = 16000

        with noalsaerr():

            p = pyaudio.PyAudio()

            stream = p.open(
                format=sample_format,
                channels=channels,
                rate=rate,
                frames_per_buffer=chunk,
                input=True,
            )

            frames = []

            while self.recording:
                data = stream.read(chunk)
                frames.append(data)

            stream.stop_stream()
            stream.close()
            p.terminate()

            audio_data = np.frombuffer(b"".join(frames), dtype=np.int16)
            audio_data_fp32 = audio_data.astype(np.float32) / 32768.0

            if self.save_audio:

                with wave.open("output.wav", "wb") as waveFile:
                    waveFile.setnchannels(channels)
                    waveFile.setsampwidth(p.get_sample_size(sample_format))
                    waveFile.setframerate(rate)
                    waveFile.writeframes(b"".join(frames))
                    waveFile.close()

            # transcribe the audio data
            text = self.transcriber.transcribe(
                audio_data_fp32,
                language=language,
            )

            print(text)


if __name__ == "__main__":
    pass
