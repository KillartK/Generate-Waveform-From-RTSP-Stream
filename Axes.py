import matplotlib.pyplot as plt
import numpy as np

class Axes:
    def __init__(self, CHUNK, threshold_negative, threshold_positive, fig, ax):
        self.CHUNK = CHUNK
        self.threshold_positive = threshold_positive
        self.threshold_negative = threshold_negative
        self.fig = fig
        self.ax = ax

    def setThresholdPositive(self, threshold_positive):
        self.threshold_positive = threshold_positive
    def setThresholdNegative(self, threshold_negative):
        self.threshold_negative = threshold_negative
    def setCHUNK(self, CHUNK):
        self.CHUNK = CHUNK

    def getFig(self):
        return self.fig

    def axes_init(self):
        # variable for plotting
        x = np.arange(0.0, 2.0 * self.CHUNK, 2.0)

        # create a line object with random data
        line, = self.ax.plot(x, np.random.rand(self.CHUNK), '-', lw=2)
        
        # basic formatting for the axes
        self.ax.set_title('AUDIO WAVEFORM')
        self.ax.set_xlabel('samples')
        self.ax.set_ylabel('amplitude')
        self.ax.set_ylim(-1.0, 1.0)
        self.ax.set_xlim(0.0, 2.0 * self.CHUNK)
        # Draw the threshold line
        self.ax.hlines(y=self.threshold_positive,linewidth=1,xmin=0, xmax=2048, color='k', linestyle = 'dashed')
        self.ax.hlines(y=self.threshold_negative,linewidth=1,xmin=0, xmax=2048, color='k', linestyle = 'dashed')
        plt.setp(self.ax, xticks=[0*1.0, 1.0*self.CHUNK, 2.0 * self.CHUNK], yticks=[-1.0, -0.5, self.threshold_negative, 0.0, self.threshold_positive, 0.5, 1.0])
        # Show the plot
        plt.show(block=False)
        return line