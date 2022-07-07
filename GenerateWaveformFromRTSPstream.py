import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from tkinter import TclError
import time
import ffmpeg
from ffpyplayer.player import MediaPlayer
# use this backend to display in separate Tk window
matplotlib.use("TkAgg")

# RTSP URL
rtsp_stream = 'rtsp://localhost:8554/stream'

# Playback audio with ffplayer
# player = MediaPlayer(rtsp_stream)

# RTSP capture with ffmpeg
stream = ffmpeg.input(rtsp_stream)
audio = stream.audio
output_audio = (
    ffmpeg
    .output(audio, '-', acodec = 'pcm_s16le', ar = 44100, ac = 1, format = 's16le')
    .run_async(pipe_stdout = True)
)

# Samples per frame
CHUNK = 2048

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
plt.setp(ax, xticks=[0*1.0, 1.0*CHUNK, 2.0 * CHUNK], yticks=[-1, -0.5, 0.0, 0.5, 1.0])

# Show the plot
plt.show(block=False)

# for measuring frame rate
frame_count = 0
start_time = time.time()
# player = MediaPlayer(rtsp_stream)
while True:
    # # Playback audio 
    # audio_framem, val = player.get_frame() 
    
    # Bytes data
    data = output_audio.stdout.read(CHUNK * 2)

    # Put data into a numpy array and convert to int16
    data_np = np.frombuffer(data, dtype=np.int16)

    # Convert data to float
    data_np = data_np.astype('float32') / 32767.0
    # print(data_np)
    # Plot data
    line.set_ydata(data_np)
    try:
        fig.canvas.draw()
        fig.canvas.flush_events()
        frame_count += 1
    except TclError:
        frame_rate = frame_count / (time.time() - start_time)
        print('stream stopped')
        print('average frame rate = {:.0f} FPS'.format(frame_rate))
        break