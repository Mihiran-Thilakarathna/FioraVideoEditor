# Import necessary parts from the moviepy library
from moviepy.editor import VideoFileClip, vfx

class FioraBackend:
    """
    This class contains all the backend functionalities for video processing.
    """
    def __init__(self):
        """
        This is the constructor method that runs when the class is initiated.
        It creates empty variables to hold the video clips.
        """
        self.clip = None
        self.original_clip = None # Added to keep the original video in memory for resets
        print("Fiora Backend Processor is ready.")

    def load_video(self, video_path):
        """
        Loads a video from the given path and assigns it to self.clip and self.original_clip.
        """
        try:
            self.clip = VideoFileClip(video_path)
            self.original_clip = VideoFileClip(video_path) # Save the original clip for resets
            print(f"Video loaded successfully: {video_path}")
            return True
        except Exception as e:
            print(f"ERROR: Could not load video. Reason: {e}")
            self.clip = None
            return False

    def export_video(self, output_path):
        """
        Saves the final processed video to the given output path.
        """
        if self.clip is None:
            print("ERROR: No processed video to export.")
            return False
        try:
            # The .write_videofile() function saves the video
            self.clip.write_videofile(output_path, codec="libx264", threads=4, preset="medium")
            print(f"Video exported successfully to: {output_path}")
            return True
        except Exception as e:
            print(f"ERROR: Could not export video. Reason: {e}")
            return False

# --- This bottom part is only for testing your backend code directly ---
if __name__ == "__main__":

    processor = FioraBackend()

    # IMPORTANT: Change this path to a real video file on your computer
    video_loaded = processor.load_video("C:/Users/YourUser/Videos/sample.mp4") # <--- CHANGE THIS PATH

    if video_loaded:
        # Export the final video (IMPORTANT: Change this path to where you want to save the output)
        processor.export_video("C:/Users/YourUser/Videos/output_video.mp4") # <--- CHANGE THIS PATH

    print("\n--- Testing complete! ---")