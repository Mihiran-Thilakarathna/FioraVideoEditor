import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip, vfx, afx, CompositeAudioClip


class FioraBackend:
    def __init__(self):
        # Current, actively displayed clips that have effects applied
        self.clip = None
        self.main_audio_clip = None

        # Unmodified original clips, loaded once and never changed
        self.original_clip = None
        self.original_main_audio = None

        # Base clips that hold the trimmed state, but no other visual/audio effects
        # All effects are applied to these base clips to avoid compounding issues.
        self.base_clip = None
        self.base_main_audio = None

        # Lists for additional audio tracks
        self.additional_audio_clips = []
        self.original_additional_audio_clips = []

        # Dictionary to hold all adjustment states (e.g., brightness, contrast)
        self.adjustments = {
            "brightness": 0.0, "contrast": 0.0, "gamma": 1.0,
            "r": 1.0, "g": 1.0, "b": 1.0,
            "volume": 1.0, "speed": 1.0
        }
        print("Fiora Backend Processor is ready.")

    def close(self):
        """
        Safely closes all moviepy clip resources.
        This is very important to release file handles and prevent errors
        when loading a new video.
        """
        print("Closing existing video/audio resources...")
        clips_to_close = [
            self.clip, self.original_clip, self.base_clip,
            self.main_audio_clip, self.original_main_audio, self.base_main_audio
        ]
        clips_to_close.extend(self.additional_audio_clips)
        clips_to_close.extend(self.original_additional_audio_clips)

        for clip in clips_to_close:
            if clip:
                try:
                    # moviepy clips have a close() method to terminate their ffmpeg subprocess
                    clip.close()
                except Exception as e:
                    print(f"Error closing a clip: {e}")

    def load_video(self, video_path):
        try:
            # First, close any resources from a previously loaded video to prevent errors.
            self.close()

            # Now, re-initialize the state for the new video.
            self.__init__()

            clip = VideoFileClip(video_path)
            self.original_clip = clip
            self.base_clip = clip
            self.clip = clip

            if clip.audio:
                self.original_main_audio = clip.audio
                self.base_main_audio = clip.audio
                self.main_audio_clip = clip.audio
            return True
        except Exception as e:
            print(f"ERROR: Could not load video. Reason: {e}")
            return False

    def load_audio(self, audio_path):
        """Adds a new audio track, trimmed to match the current video clip's duration."""
        try:
            new_clip = AudioFileClip(audio_path)

            # If a video is loaded, trim the new audio to fit the video's current length.
            if self.clip:
                if new_clip.duration > self.clip.duration:
                    new_clip = new_clip.subclip(0, self.clip.duration)

            self.additional_audio_clips.append(new_clip)
            self.original_additional_audio_clips.append(AudioFileClip(audio_path))
            return len(self.additional_audio_clips)
        except Exception as e:
            print(f"ERROR: Could not load audio. Reason: {e}")
            return 0

    def apply_all_effects(self):
        """
        Applies all adjustments from the self.adjustments dictionary
        to the base (trimmed) clip. This prevents compounding effects and performance issues.
        """
        if not self.base_clip: return

        # Always start from the clean, trimmed base clip to apply effects.
        temp_clip = self.base_clip
        temp_main_audio = self.base_main_audio

        # Get all current adjustment values.
        lum = self.adjustments.get("brightness", 0.0)
        con = self.adjustments.get("contrast", 0.0)
        gamma = self.adjustments.get("gamma", 1.0)
        r, g, b = self.adjustments.get("r", 1.0), self.adjustments.get("g", 1.0), self.adjustments.get("b", 1.0)

        # Apply visual effects one by one.
        if lum != 0.0 or con != 0.0: temp_clip = temp_clip.fx(vfx.lum_contrast, lum=lum, contrast=con)
        if gamma != 1.0: temp_clip = temp_clip.fx(vfx.gamma_corr, gamma=gamma)
        if r != 1.0 or g != 1.0 or b != 1.0:
            temp_clip = temp_clip.fl_image(lambda frame: self._rgb_manipulator(frame, r, g, b))

        # Update the active clip that is shown in the UI.
        self.clip = temp_clip

        # Apply audio effects.
        if temp_main_audio:
            volume = self.adjustments.get("volume", 1.0)
            if volume != 1.0:
                self.main_audio_clip = temp_main_audio.fx(afx.volumex, volume)
            else:
                self.main_audio_clip = temp_main_audio

    @staticmethod
    def _rgb_manipulator(frame, r, g, b):
        """A helper function to change the Red, Green, and Blue values of a video frame."""
        new_frame = frame.astype('float64')
        new_frame[:, :, 0] *= r
        new_frame[:, :, 1] *= g
        new_frame[:, :, 2] *= b
        return np.clip(new_frame, 0, 255).astype('uint8')

    def set_adjustment(self, key, value):
        """Updates an adjustment value (like brightness) and reapplies all effects."""
        if self.original_clip:
            self.adjustments[key] = value
            self.apply_all_effects()

    def reset_all_changes(self):
        """Resets all clips and adjustments back to their original state."""
        if self.original_clip:
            # Reset all clip versions to the original video.
            self.clip = self.original_clip
            self.base_clip = self.original_clip
            self.main_audio_clip = self.original_main_audio
            self.base_main_audio = self.original_main_audio

            # Clear any extra audio tracks.
            self.additional_audio_clips.clear()
            self.original_additional_audio_clips.clear()

            # Reset the adjustments dictionary to default values.
            for key in self.adjustments:
                if key in ["r", "g", "b", "gamma", "volume", "speed"]:
                    self.adjustments[key] = 1.0
                else:
                    self.adjustments[key] = 0.0
            print("All changes have been reset.")
            # After resetting, apply the default (empty) effects to update the view.
            self.apply_all_effects()
            return True
        return False

    def trim_video(self, start, end):
        """Trims the video and all associated audio tracks."""
        if not self.clip: return False
        try:
            current_duration = self.base_clip.duration
            if start >= end or start > current_duration:
                print("Invalid trim values.")
                return False

            end = min(end, current_duration)

            # The trim is applied to the 'base' clips.
            self.base_clip = self.base_clip.subclip(start, end)
            if self.base_main_audio:
                if start < self.base_main_audio.duration:
                    self.base_main_audio = self.base_main_audio.subclip(start, min(end, self.base_main_audio.duration))

            # Trim any additional audio tracks as well.
            trimmed_additional = []
            for audio in self.additional_audio_clips:
                if start < audio.duration:
                    audio_end = min(end, audio.duration)
                    trimmed_additional.append(audio.subclip(start, audio_end))
            self.additional_audio_clips = trimmed_additional

            # Re-apply all current effects to the newly trimmed base clip.
            self.apply_all_effects()
            return True
        except Exception as e:
            print(f"ERROR during trim: {e}")
            return False

    def apply_filter(self, filter_name):
        """Applies a permanent filter to the video."""
        if not self.clip: return
        # Filters are applied directly to the base_clip.
        if filter_name == 'grayscale':
            self.base_clip = self.base_clip.fx(vfx.blackwhite)
        elif filter_name == 'invert_colors':
            self.base_clip = self.base_clip.fx(vfx.invert_colors)
        elif filter_name == 'mirror_x':
            self.base_clip = self.base_clip.fx(vfx.mirror_x)
        # Re-apply adjustments on top of the new filtered base.
        self.apply_all_effects()

    def export_video(self, output_path):
        """Exports the final edited video to a file."""
        if not self.clip: return False
        try:
            final_clip = self.clip
            all_audio_tracks = []

            if self.main_audio_clip:
                adjusted_main_audio = self.main_audio_clip.set_duration(self.clip.duration)
                all_audio_tracks.append(adjusted_main_audio)

            for aud_clip in self.additional_audio_clips:
                all_audio_tracks.append(aud_clip.set_duration(self.clip.duration))

            # Combine all audio tracks if there are any.
            if all_audio_tracks:
                final_audio = CompositeAudioClip(all_audio_tracks)
                final_clip = final_clip.set_audio(final_audio)

            # Write the final video file with a progress bar in the console.
            final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac",
                                       threads=4, preset="medium", logger='bar')
            return True
        except Exception as e:
            print(f"ERROR: Could not export video. Reason: {e}")
            return False
