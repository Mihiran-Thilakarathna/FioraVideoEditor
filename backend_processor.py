from moviepy.editor import VideoFileClip, AudioFileClip, vfx


class FioraBackend:
    def __init__(self):
        self.clip = None
        self.audio_clip = None
        self.original_clip = None
        self.adjustments = {"brightness": 0.0, "contrast": 0.0, "gamma": 1.0}
        print("Fiora Backend Processor is ready.")

    def load_video(self, video_path):
        try:
            self.clip = VideoFileClip(video_path)
            self.original_clip = VideoFileClip(video_path)
            if self.clip.audio:
                self.audio_clip = self.clip.audio
            return True
        except Exception as e:
            print(f"ERROR: Could not load video. Reason: {e}")
            self.clip = None
            return False

    def load_audio(self, audio_path):
        try:
            self.audio_clip = AudioFileClip(audio_path)
            return True
        except Exception as e:
            print(f"ERROR: Could not load audio. Reason: {e}")
            self.audio_clip = None
            return False

    def apply_all_adjustments(self):
        if not self.original_clip: return
        temp_clip = self.original_clip
        lum = self.adjustments.get("brightness", 0.0)
        con = self.adjustments.get("contrast", 0.0)
        if lum != 0.0 or con != 0.0:
            temp_clip = temp_clip.fx(vfx.lum_contrast, lum=lum, contrast=con)
        gamma = self.adjustments.get("gamma", 1.0)
        if gamma != 1.0:
            temp_clip = temp_clip.fx(vfx.gamma_corr, gamma=gamma)
        self.clip = temp_clip

    def set_adjustment(self, key, value):
        if self.original_clip:
            self.adjustments[key] = value
            self.apply_all_adjustments()

    def trim_video(self, start, end):
        if not self.clip: return False
        try:
            self.clip = self.clip.subclip(start, end)
            self.original_clip = self.original_clip.subclip(start, end)
            if self.audio_clip and self.audio_clip.duration > end:
                self.audio_clip = self.audio_clip.subclip(start, end)
            return True
        except Exception as e:
            print(f"ERROR during trim: {e}")
            return False

    def apply_grayscale_filter(self):
        if self.clip:
            self.clip = self.clip.fx(vfx.blackwhite)

    def export_video(self, output_path):
        if self.clip is None: return False
        try:
            final_clip_to_write = self.clip
            # If a separate audio clip exists, adjust its duration to match the video clip
            if self.audio_clip:
                # If audio is longer than video, trim it. If shorter, it will loop or stop. set_duration is explicit.
                adjusted_audio = self.audio_clip.set_duration(self.clip.duration)
                final_clip_to_write = self.clip.set_audio(adjusted_audio)

            final_clip_to_write.write_videofile(output_path, codec="libx264", threads=4, preset="medium")
            return True
        except Exception as e:
            print(f"ERROR: Could not export video. Reason: {e}")
            return False