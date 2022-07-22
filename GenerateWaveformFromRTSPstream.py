import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from tkinter import TclError
import time
import ffmpeg
from ffpyplayer.player import MediaPlayer
import multiprocessing
import io
import sys
import pyaudio
import subprocess as sp
FFMPEG_BIN = "ffmpeg.exe"
# use this backend to display in separate window
matplotlib.use("tkagg")

# RTSP stream input
# rtsp_stream = input('Enter your rtsp stream: ')

# Samples per frame
CHUNK = 512

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
ax.axhline(y=threshold_positive,linewidth=1, color='k', linestyle = 'dashed')
ax.axhline(y=threshold_negative,linewidth=1, color='k', linestyle = 'dashed')
plt.setp(ax, xticks=[0*1.0, 1.0*CHUNK, 2.0 * CHUNK], yticks=[-1.0, -0.5, threshold_negative, 0.0, threshold_positive, 0.5, 1.0])
# Show the plot
plt.show(block=False)

# Capture RTSP stream 
stream = ffmpeg.input('rtsp://localhost:8554/stream')
audio = stream.audio 
output_audio = (
    ffmpeg
    .output(audio, '-', acodec = 'pcm_f32le', ar = 44100, ac = 1, format = 'f32le')
    .run_async(pipe_stdout = True)
)

 
# while True:
#     try: 
#         audio_data = output_audio.read(CHUNK * 2)
#     except IOError:
#         print("No data")
#         break
def callback(in_data, frame_count, time_info, status):
    data = np.frombuffer(output_audio.stdout.read(4096), dtype="float32")
    # data = data.reshape((len(data)//2,2))
    #data = pipe.readbuffer(frame_count)
    return (data, pyaudio.paContinue)
 
# open stream using callback (3)
p = pyaudio.PyAudio()
audio_stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                output=True,
                input=True,
                stream_callback=callback)
 

# Capture rtsp stream and plot the waveform
def plotWaveform():
    # Start Plotting
    while True:
        # Put data into a numpy array and convert to int16
        data_np = np.frombuffer(audio_stream.read(CHUNK * 2), dtype=np.float32)
        # Convert data to float
        # Plot data
        line.set_ydata(data_np)
        fig.canvas.draw()
        fig.canvas.flush_events()
def playAudio():
    audio_stream.start_stream()
    while audio_stream.is_active():
        time.sleep(0.5)
    audio_stream.stop_stream()
    audio_stream.close()
    p.terminate()

p2 = multiprocessing.Process(target=plotWaveform())
p1 = multiprocessing.Process(target=playAudio())

p1.start()
p2.start()
