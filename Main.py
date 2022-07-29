from Axes import Axes
from RtspStream import RtspStream
import PlotWaveform
import matplotlib.pyplot as plt
import matplotlib
import Constant

# Use this backend to display in separate window
matplotlib.use("tkagg")

if __name__ == '__main__':
    RTSP_STREAM = input("Enter rtsp stream URL: ")

    # RTSP stream capture and tranfer to stdout
    audio_output = RtspStream(RTSP_STREAM, Constant.SAMPLE_RATE).capture_rtsp_stream()

    # Axes init and format 
    fig, ax = plt.subplots(1, figsize=(10, 4))
    line = Axes(Constant.CHUNK, Constant.THRESHOLD_NEGATIVE, Constant.THRESHOLD_POSITIVE, fig, ax).axes_init()

    PlotWaveform.plotWaveform(audio_output, fig, line)