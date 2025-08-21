import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip, vfx, afx


class FioraBackend:
    def __init__(self):
        self.clip = None
        self.audio_clip = None
        self.original_clip = None
        self.original_audio = None

        # Dictionary to hold all adjustment states
        self.adjustments = {
            "brightness": 0.0, "contrast": 0.0, "gamma": 1.0,
            "r": 1.0, "g": 1.0, "b": 1.0,
            "volume": 1.0, "speed": 1.0
        }
        print("Fiora Backend Processor is ready.")

    def load_video(self, video_path):
        try:
            self.clip = VideoFileClip(video_path)
            self.original_clip = VideoFileClip(video_path)
            if self.clip.audio:
                self.audio_clip = self.clip.audio
                self.original_audio = self.clip.audio
            return True
        except Exception as e:
            print(f"ERROR: Could not load video. Reason: {e}")
            return False

    def load_audio(self, audio_path):
        try:
            self.audio_clip = AudioFileClip(audio_path)
            self.original_audio = AudioFileClip(audio_path)
            return True
        except Exception as e:
            print(f"ERROR: Could not load audio. Reason: {e}")
            return False

    def apply_all_effects(self):
        """Applies all stored adjustments to the original clip."""
        if not self.original_clip: return

        temp_clip = self.original_clip
        temp_audio = self.original_audio

        # Apply visual effects (vfx)
        lum = self.adjustments.get("brightness", 0.0)
        con = self.adjustments.get("contrast", 0.0)
        gamma = self.adjustments.get("gamma", 1.0)
        r, g, b = self.adjustments.get("r", 1.0), self.adjustments.get("g", 1.0), self.adjustments.get("b", 1.0)
        speed = self.adjustments.get("speed", 1.0)

        if lum != 0.0 or con != 0.0: temp_clip = temp_clip.fx(vfx.lum_contrast, lum=lum, contrast=con)
        if gamma != 1.0: temp_clip = temp_clip.fx(vfx.gamma_corr, gamma=gamma)
        if r != 1.0 or g != 1.0 or b != 1.0:
            temp_clip = temp_clip.fl_image(lambda frame: self._rgb_manipulator(frame, r, g, b))
        if speed != 1.0:
            temp_clip = temp_clip.fx(vfx.speedx, speed)
            if temp_audio: temp_audio = temp_audio.fx(afx.speedx, speed)

        self.clip = temp_clip

        # Apply audio effects (afx)
        if temp_audio:
            volume = self.adjustments.get("volume", 1.0)
            if volume != 1.0:
                temp_audio = temp_audio.fx(afx.volumex, volume)
            self.audio_clip = temp_audio

    @staticmethod
    def _rgb_manipulator(frame, r, g, b):
        """
        Static method to manipulate RGB values of a frame.
        It doesn't need access to 'self'.
        """
        new_frame = frame.astype('float64')
        new_frame[:, :, 0] *= r
        new_frame[:, :, 1] *= g
        new_frame[:, :, 2] *= b
        return np.clip(new_frame, 0, 255).astype('uint8')

    def set_adjustment(self, key, value):
        if self.original_clip:
            self.adjustments[key] = value
            self.apply_all_effects()

    def reset_all_changes(self):
        if self.original_clip:
            self.clip = self.original_clip
            self.audio_clip = self.original_audio
            # Reset adjustments dictionary to defaults
            for key in self.adjustments:
                if key in ["r", "g", "b", "gamma", "volume", "speed"]:
                    self.adjustments[key] = 1.0
                else:
                    self.adjustments[key] = 0.0
            print("All changes have been reset.")
            return True
        return False

    def trim_video(self, start, end):
        """
        FIXED: This function now only modifies the current working clip (`self.clip`),
        leaving the backup (`self.original_clip`) untouched.
        """
        if not self.clip: return False
        try:
            # Apply all current adjustments to the original clip first
            self.apply_all_effects()

            # Now, trim the already-adjusted clip
            self.clip = self.clip.subclip(start, end)

            # Also trim the audio clip if it exists
            if self.audio_clip and self.audio_clip.duration > end:
                self.audio_clip = self.audio_clip.subclip(start, end)

            return True
        except Exception as e:
            print(f"ERROR during trim: {e}")
            return False

    def apply_filter(self, filter_name):
        if not self.clip: return
        if filter_name == 'grayscale':
            self.clip = self.clip.fx(vfx.blackwhite)
        elif filter_name == 'invert_colors':
            self.clip = self.clip.fx(vfx.invert_colors)
        elif filter_name == 'mirror_x':
            self.clip = self.clip.fx(vfx.mirror_x)

    def export_video(self, output_path):
        if not self.clip: return False
        try:
            final_clip = self.clip
            if self.audio_clip:
                adjusted_audio = self.audio_clip.set_duration(self.clip.duration)
                final_clip = self.clip.set_audio(adjusted_audio)
            final_clip.write_videofile(output_path, codec="libx264", threads=4, preset="medium")
            return True
        except Exception as e:
            print(f"ERROR: Could not export video. Reason: {e}")
            return False
