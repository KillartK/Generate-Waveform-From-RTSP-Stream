import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import ffmpeg
import pyaudio

# use this backend to display in separate window
matplotlib.use("tkagg")

# RTSP stream input
rtsp_stream = input('Enter your rtsp stream: ')

# Samples per frame
CHUNK = 1024

# Plot sizes
fig, ax = plt.subplots(1, figsize=(10, 4))

# variable for plotting
x = np.arange(0.0, 2.0 * CHUNK, 2.0)

# create a line object with random data
line, = ax.plot(x, np.random.rand(CHUNK), '-', lw=2)

# basic formatting for the axes
ax.set_title('AUDIO WAVEFORM')
ax.set_xlabel('samples')
ax.set_ylabel('amplitude')
ax.set_ylim(-1.0, 1.0)
ax.set_xlim(0.0, 2.0 * CHUNK)
# Draw the threshold line
threshold_positive = 0.25
threshold_negative = -0.25
ax.hlines(y=threshold_positive,linewidth=1,xmin=0, xmax=2048, color='k', linestyle = 'dashed')
ax.hlines(y=threshold_negative,linewidth=1,xmin=0, xmax=2048, color='k', linestyle = 'dashed')
plt.setp(ax, xticks=[0*1.0, 1.0*CHUNK, 2.0 * CHUNK], yticks=[-1.0, -0.5, threshold_negative, 0.0, threshold_positive, 0.5, 1.0])
# Show the plot
plt.show(block=False)

# Capture RTSP stream 
try:
    stream = ffmpeg.input(rtsp_stream)
    audio = stream.audio 
    output_audio = (
        ffmpeg
        .output(audio, '-', acodec = 'pcm_s16le', ar = 22050, ac = 1, format = 's16le')
        .run_async(pipe_stdout = True)
    )
except Exception:
    print("No input found")

# Create a pyaudio output stream to write audio data
p = pyaudio.PyAudio()
audio_stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=22050,
                output=True,
                )

# Plot the waveform
def plotWaveform():
    while True:
        try:
            # Read data from buffer
            audio_data = output_audio.stdout.read(CHUNK * 2)
            # Play audio with data from buffer
            audio_stream.write(audio_data)

            # Convert data from buffer to float32 
            data_np = np.frombuffer(audio_data, dtype=np.int16)
            data_np = data_np.astype('float32')/32767.0

            # Plot data
            line.set_ydata(data_np)
            fig.canvas.draw()
            fig.canvas.flush_events()
        except Exception:
            print('No data captured')
            break
if __name__ == '__main__':
    plotWaveform()
    p.terminate