import pyaudio

class AudioStream:
    def __init__(self, SAMPLE_RATE):
        self.SAMPLE_RATE = SAMPLE_RATE
        
    def audio_stream_create(self):
        p = pyaudio.PyAudio()
        audio_stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=self.SAMPLE_RATE,
                        output=True,
                        )
        return audio_stream