import Constant
import numpy as np
from AudioStream import AudioStream

audio_stream = AudioStream(Constant.SAMPLE_RATE).audio_stream_create()

def plotWaveform(audio_output, fig, line):
    while True:
        try:
            # Read data from buffer
            audio_data = audio_output.stdout.read(Constant.CHUNK * 2)

            # Play audio with data from buffer
            audio_stream.write(audio_data)

            # Convert data from buffer to float32 
            data_np = np.frombuffer(audio_data, dtype=np.int16)
            data_np = data_np.astype('float32')/32767.0

            # Plot data to waveform
            line.set_ydata(data_np)
            fig.canvas.draw()
            fig.canvas.flush_events()
        except Exception:
            print('No data captured')
            break