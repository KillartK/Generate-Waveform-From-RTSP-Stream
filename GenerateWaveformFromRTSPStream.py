import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import ffmpeg
import pyaudio

# use this backend to display in separate window
matplotlib.use("tkagg")

# Samples per frame and sample rate
CHUNK = 1024
SAMPLE_RATE = 22050

# Axe init and format
def axe_format(ax):   
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
    return line

# Capture RTSP stream 
def RTSP_Capture(rtsp_stream):
    try:
        stream = ffmpeg.input(rtsp_stream)
        audio = stream.audio 
        output_audio = (
            ffmpeg
            .output(audio, '-', acodec = 'pcm_s16le', ar = SAMPLE_RATE, ac = 1, format = 's16le')
            .run_async(pipe_stdout = True)
        )
    except Exception:
        print("No input found")
    return output_audio

# Create a pyaudio output stream object to write audio data 
def audio_stream_create():
    p = pyaudio.PyAudio()
    audio_stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=SAMPLE_RATE,
                    output=True,
                    )
    return audio_stream

# Plot the waveform
def plot_waveform(output_audio, audio_stream, fig, line):
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
            print
            ('No data captured')
            break

if __name__ == '__main__':
    # RTSP stream input
    rtsp_stream = input("Enter rtsp stream URL: ")

    output_audio = RTSP_Capture(rtsp_stream)
    audio_stream = audio_stream_create()

    # figure size 
    fig, ax = plt.subplots(1, figsize=(10, 4))
    line = axe_format(ax)

    plot_waveform(output_audio, audio_stream, fig, line)