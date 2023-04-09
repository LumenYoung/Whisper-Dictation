import pyaudio
import wave
import numpy as np
import time
import threading
from typing import List, Dict, Any

class Audio(object):
    """An audio object to record the microphone.
    """
    
    def __init__(self, save_audio: Any = False) -> None:
        self.recording = False

        self.save_audio = save_audio

        
    # the start function implement the function to start recording
    def start(self, language:str) -> None:
        # start a new thread to record the audio
        thread = threading.Thread(target=self._record, args=(language,))
        thread.start()

    # the stop function implement the function to stop recording
    def stop(self) -> None:
        self.recording = False
    
    # the record function implement the function to record
    def _record(self, language:str) -> None:
        
        self.recording = True
        # audio parameters
        chunk = 1024
        sample_format = pyaudio.paInt16
        channels = 1
        rate = 16000
        record_seconds = 5
        
        p = pyaudio.PyAudio()

        stream  = p.open(format=sample_format,
                        channels=channels,
                        rate=rate,
                        frames_per_buffer=chunk,
                        input=True,
                        # input_device_index=22
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
            

        
def trying():
    
    p = pyaudio.PyAudio()
    
    # audio parameters
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    rate = 16000
    record_seconds = 5
    
    devices: List[Dict] = [p.get_device_info_by_index(i) for i in range(p.get_device_count())]
    
    # get speaker devices from the system
    speakers:List[Dict] = [device for device in devices if device["maxOutputChannels"] > 0]
    
    # stream from the index 22
    stream  = p.open(format=sample_format,
                    channels=channels,
                    rate=rate,
                    frames_per_buffer=chunk,
                    input=True,
                    # input_device_index=22
                    )
    
    print("Recording...")
    
    frames = []

    for i in range(0, int(rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()

    p.terminate()

    print("Finished recording")

    # save the recorded data as a WAV file
    # waveFile = wave.open("output.wav", "wb")
    # waveFile.setnchannels(channels)
    # waveFile.setsampwidth(p.get_sample_size(sample_format))
    # waveFile.setframerate(rate)
    # waveFile.writeframes(b"".join(frames))
    # waveFile.close()
    
    # rewrite the above code using with statement
    with wave.open("output.wav", "wb") as waveFile:
        waveFile.setnchannels(channels)
        waveFile.setsampwidth(p.get_sample_size(sample_format))
        waveFile.setframerate(rate)
        waveFile.writeframes(b"".join(frames))
    





if __name__ == "__main__":
    audio = Audio(save_audio=True)
    audio.start("en")
    # wait for 5 seconds
    time.sleep(5)

    audio.stop()