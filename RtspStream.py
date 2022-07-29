import ffmpeg
class RtspStream:
    def __init__(self, rtsp_stream_URl, SAMPLE_RATE):
        self.rtsp_stream_URL = rtsp_stream_URl
        self.SAMPLE_RATE = SAMPLE_RATE
    def capture_rtsp_stream(self):
        try:
            stream = ffmpeg.input(self.rtsp_stream_URL)
            audio = stream.audio 
            output_audio = (
                ffmpeg
                .output(audio, '-', acodec = 'pcm_s16le', ar = self.SAMPLE_RATE, ac = 1, format = 's16le')
                .run_async(pipe_stdout = True)
            )
        except Exception:
            print("No input found")
        return output_audio
