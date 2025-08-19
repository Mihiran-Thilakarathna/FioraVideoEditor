import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip, vfx, CompositeAudioClip


class FioraBackend:
    def __init__(self):
        # --- CHANGED: Renamed original_clip to source_clip to hold the pristine video file
        self.source_clip = None  # The absolute original video file, never modified
        self.clip = None  # The currently processed clip for preview

        self.video_audio = None
        self.external_audio = None

        # --- NEW: State variables to store all edits
        self.trim_start = 0.0
        self.trim_end = 0.0
        self.applied_filters = []
        self.adjustments = {
            "brightness": 0.0, "contrast": 0.0, "gamma": 1.0,
            "r": 1.0, "g": 1.0, "b": 1.0, "volume": 1.0, "speed": 1.0
        }
        print("Fiora Backend Processor is ready.")

    def close_all_clips(self):
        # --- CHANGED: Closes all clips including the new source_clip
        if self.clip: self.clip.close()
        if self.source_clip: self.source_clip.close()
        if self.video_audio: self.video_audio.close()
        if self.external_audio: self.external_audio.close()

    def load_video(self, video_path):
        try:
            self.close_all_clips()
            self.__init__()  # Reset the entire state

            # --- CHANGED: Loads video into source_clip
            self.source_clip = VideoFileClip(video_path)
            self.clip = self.source_clip.copy()

            # --- NEW: Initialize trim times to the full duration
            self.trim_start = 0.0
            self.trim_end = self.source_clip.duration

            if self.clip.audio:
                self.video_audio = self.clip.audio
            return True
        except Exception as e:
            print(f"ERROR: Could not load video. Reason: {e}")
            return False

    def load_audio(self, audio_path):
        try:
            if self.external_audio: self.external_audio.close()
            self.external_audio = AudioFileClip(audio_path)
            return True
        except Exception as e:
            print(f"ERROR: Could not load audio. Reason: {e}")
            return False

    # --- REBUILT: This is the core function that rebuilds the clip from scratch on every change
    def apply_all_effects(self):
        if not self.source_clip: return

        # 1. Start with a fresh subclip from the absolute original source
        temp_clip = self.source_clip.subclip(self.trim_start, self.trim_end)

        # 2. Apply adjustments (brightness, color, etc.)
        lum = self.adjustments.get("brightness", 0.0)
        con = self.adjustments.get("contrast", 0.0)
        gamma = self.adjustments.get("gamma", 1.0)
        r, g, b = self.adjustments.get("r", 1.0), self.adjustments.get("g", 1.0), self.adjustments.get("b", 1.0)
        speed = self.adjustments.get("speed", 1.0)

        if lum != 0.0 or con != 0.0: temp_clip = temp_clip.fx(vfx.lum_contrast, lum=lum, contrast=con)
        if gamma != 1.0: temp_clip = temp_clip.fx(vfx.gamma_corr, gamma=gamma)
        if r != 1.0 or g != 1.0 or b != 1.0:
            temp_clip = temp_clip.fl_image(lambda frame: self._rgb_manipulator(frame, r, g, b))

        # 3. Apply filters from the list
        for f in self.applied_filters:
            if f == 'grayscale':
                temp_clip = temp_clip.fx(vfx.blackwhite)
            elif f == 'mirror_x':
                temp_clip = temp_clip.fx(vfx.mirror_x)

        if speed != 1.0: temp_clip = temp_clip.fx(vfx.speedx, speed)

        # 4. Replace the old preview clip with the newly generated one
        if self.clip: self.clip.close()
        self.clip = temp_clip

        # 5. Update the associated audio track
        if self.clip.audio:
            self.video_audio = self.clip.audio

    @staticmethod
    def _rgb_manipulator(frame, r, g, b):
        new_frame = frame.astype('float64')
        new_frame[:, :, 0] *= r;
        new_frame[:, :, 1] *= g;
        new_frame[:, :, 2] *= b
        return np.clip(new_frame, 0, 255).astype('uint8')

    # --- CHANGED: Now just updates the state and calls the main effect function
    def set_adjustment(self, key, value):
        if self.source_clip:
            self.adjustments[key] = value
            self.apply_all_effects()

    # --- REBUILT: Resets all state variables to their defaults and rebuilds the clip
    def reset_all_changes(self):
        if self.source_clip:
            # Reset adjustments dictionary
            for key in self.adjustments:
                self.adjustments[key] = 1.0 if key in ["r", "g", "b", "gamma", "volume", "speed"] else 0.0

            # Reset filters and trim times
            self.applied_filters = []
            self.trim_start = 0.0
            self.trim_end = self.source_clip.duration

            # Clear external audio
            if self.external_audio: self.external_audio.close()
            self.external_audio = None

            # Rebuild the clip to its original state
            self.apply_all_effects()
            print("All changes have been reset.")
            return True
        return False

    # --- REBUILT: Now only updates the trim times and calls the main effect function
    def trim_video(self, start, end):
        if not self.source_clip: return False
        try:
            # Validate times against the source clip's duration
            start_time = max(0, float(start))
            end_time = min(self.source_clip.duration, float(end))

            if start_time >= end_time:
                print(f"ERROR: Invalid trim times. Start ({start_time}) must be less than End ({end_time}).")
                return False

            self.trim_start = start_time
            self.trim_end = end_time
            self.apply_all_effects()
            return True
        except Exception as e:
            print(f"ERROR during trim: {e}")
            return False

    # --- REBUILT: Adds the filter to a list and calls the main effect function
    def apply_filter(self, filter_name):
        if not self.source_clip: return

        # Avoid adding the same filter multiple times
        if filter_name not in self.applied_filters:
            self.applied_filters.append(filter_name)
            self.apply_all_effects()

    def export_video(self, output_path):
        if not self.clip: return False
        try:
            final_clip_to_export = self.clip

            # Determine which audio to use
            active_audio = None
            if self.external_audio:
                active_audio = self.external_audio
            elif self.video_audio:
                active_audio = self.video_audio

            if active_audio:
                # Adjust audio duration to match the final video clip's duration
                if active_audio.duration > final_clip_to_export.duration:
                    active_audio = active_audio.subclip(0, final_clip_to_export.duration)

                final_clip_to_export = final_clip_to_export.set_audio(active_audio)
            else:
                # Ensure there is no audio if none is available
                final_clip_to_export.audio = None

            final_clip_to_export.write_videofile(output_path, codec="libx264", threads=4, preset="medium")
            return True
        except Exception as e:
            print(f"ERROR: Could not export video. Reason: {e}")
            return False
