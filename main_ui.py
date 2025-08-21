import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from backend_processor import FioraBackend
from PIL import Image, ImageTk
import os


class VideoEditorUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Fiora Editor")
        self.master.geometry("1200x750")
        self.master.minsize(900, 600)

        # --- Theme and Colors ---
        self.BG_COLOR = "#2e2e2e"
        self.FRAME_COLOR = "#252628"
        self.BUTTON_COLOR = "#3c3c3c"
        self.TEXT_COLOR = "#ffffff"
        self.ACCENT_COLOR_VIDEO = "#8e44ad"
        self.ACCENT_COLOR_AUDIO = "#27ae60"
        self.master.configure(bg=self.BG_COLOR)

        # Create an instance of the backend to handle all video processing
        self.processor = FioraBackend()

        # UI state variables
        self.status_var = tk.StringVar(value="Welcome to Fiora Editor!")
        self.pixels_per_second = 20
        self.current_time = 0.0
        self.playhead_id = None
        self.icons = {}
        self.sliders = {}
        self.is_playing = False

        try:
            icon_path = os.path.join("assets", "Fiora.png")
            app_icon = tk.PhotoImage(file=icon_path)
            self.master.iconphoto(False, app_icon)
        except tk.TclError:
            print("Icon not found: Please ensure 'Fiora.png' is in the 'assets' folder.")

        self._load_icons()
        self._create_widgets()

    def _load_icons(self):
        """Loads all icon images from the 'assets' folder."""
        icon_names = ["import", "export", "trim", "adjust", "filters", "color", "reset"]
        for name in icon_names:
            path = ""
            try:
                path = os.path.join("assets", f"{name}_icon.png")
                self.icons[name] = ImageTk.PhotoImage(Image.open(path).resize((20, 20), Image.Resampling.LANCZOS))
            except FileNotFoundError:
                print(f"Warning: Icon file not found at {path}")
                self.icons[name] = None

    def _create_widgets(self):
        """Creates and arranges all the main UI components."""
        # --- Style Configuration ---
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", padding=8, relief="flat", background=self.BUTTON_COLOR, foreground=self.TEXT_COLOR,
                        font=('Segoe UI', 10))
        style.map("TButton", background=[('active', '#4c4c4c')])
        style.configure("TFrame", background=self.FRAME_COLOR)
        style.configure("TLabel", background=self.FRAME_COLOR, foreground=self.TEXT_COLOR, font=('Segoe UI', 10))
        style.configure("TScale", background=self.FRAME_COLOR)
        style.configure("Header.TLabel", font=('Segoe UI', 11, 'bold'))

        # --- Main Layout (Paned Windows) ---
        main_paned = ttk.Panedwindow(self.master, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=8, pady=(8, 0))

        left_frame = ttk.Frame(main_paned, width=150)
        left_frame.pack_propagate(False)
        main_paned.add(left_frame)
        mid_paned = ttk.Panedwindow(main_paned, orient=tk.VERTICAL)
        main_paned.add(mid_paned, weight=1)
        self.right_frame = ttk.Frame(main_paned, width=300)
        self.right_frame.pack_propagate(False)
        main_paned.add(self.right_frame)

        self.right_content_frame = ttk.Frame(self.right_frame)
        self.right_content_frame.pack(fill=tk.BOTH, expand=True)

        # --- Right Panel Buttons ---
        bottom_buttons_frame = ttk.Frame(self.right_frame)
        bottom_buttons_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10, padx=10)
        ttk.Button(bottom_buttons_frame, text=" Reset All", image=self.icons.get("reset"), compound="left",
                   command=self._reset_all).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(bottom_buttons_frame, text=" Export Video", image=self.icons.get("export"), compound="left",
                   command=self._export_video).pack(fill=tk.X)

        # --- Left Toolbar Buttons ---
        ttk.Button(left_frame, text=" Import Video", image=self.icons.get("import"), compound="left",
                   command=self._load_video).pack(fill=tk.X, pady=6, padx=6)
        ttk.Button(left_frame, text=" Import Audio", image=self.icons.get("import"), compound="left",
                   command=self._load_audio).pack(fill=tk.X, pady=6, padx=6)
        ttk.Separator(left_frame, orient='horizontal').pack(fill='x', pady=10, padx=5)
        ttk.Label(left_frame, text="Tools").pack()
        ttk.Button(left_frame, text=" Trim", image=self.icons.get("trim"), compound="left",
                   command=self._show_trim_panel).pack(fill=tk.X, pady=6, padx=6)
        ttk.Button(left_frame, text=" Light", image=self.icons.get("adjust"), compound="left",
                   command=self._show_adjust_panel).pack(fill=tk.X, pady=6, padx=6)
        ttk.Button(left_frame, text=" Colour", image=self.icons.get("color"), compound="left",
                   command=self._show_color_panel).pack(fill=tk.X, pady=6, padx=6)
        ttk.Button(left_frame, text=" Filters", image=self.icons.get("filters"), compound="left",
                   command=self._show_filter_panel).pack(fill=tk.X, pady=6, padx=6)

        # --- Center Panel (Preview and Timeline) ---
        preview_container = ttk.Frame(mid_paned)
        mid_paned.add(preview_container, weight=5)
        self.preview_canvas = tk.Canvas(preview_container, bg="black", highlightthickness=0)
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)
        self.preview_canvas.bind("<Configure>", self._resize_preview)
        self.tk_image = None

        controls_frame = ttk.Frame(preview_container)
        controls_frame.pack(fill=tk.X, pady=5)
        controls_frame.columnconfigure(0, weight=1)
        self.play_pause_button = ttk.Button(controls_frame, text="▶ Play", command=self._toggle_playback)
        self.play_pause_button.pack()

        timeline_panel = ttk.Frame(mid_paned, height=180)
        mid_paned.add(timeline_panel, weight=1)
        self.track_header_canvas = tk.Canvas(timeline_panel, width=80, bg=self.FRAME_COLOR, highlightthickness=0)
        self.track_header_canvas.pack(side=tk.LEFT, fill=tk.Y)
        h_scroll = ttk.Scrollbar(timeline_panel, orient=tk.HORIZONTAL)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.timeline_canvas = tk.Canvas(timeline_panel, bg="#1e1f23", highlightthickness=0,
                                         xscrollcommand=h_scroll.set)
        self.timeline_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        h_scroll.config(command=self.timeline_canvas.xview)
        self.timeline_canvas.bind("<Button-1>", self._on_timeline_click)

        # --- Final Setup ---
        self._create_all_panels()
        self._show_adjust_panel()
        status_bar = tk.Label(self.master, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self._draw_timeline()

    # --- Panel Creation and Management ---

    def _create_all_panels(self):
        """Creates all the different tool panels for the right-side frame."""
        self.trim_frame = self._create_trim_panel(self.right_content_frame)
        self.adjust_frame = self._create_adjust_panel(self.right_content_frame)
        self.color_frame = self._create_color_panel(self.right_content_frame)
        self.filter_frame = self._create_filter_panel(self.right_content_frame)

    def _clear_right_panel(self):
        """Removes all widgets from the right panel before showing a new one."""
        for widget in self.right_content_frame.winfo_children():
            widget.pack_forget()

    def _show_panel(self, panel_name, panel_widget):
        """A helper function to show a specific panel in the right frame."""
        self._clear_right_panel()
        ttk.Label(self.right_content_frame, text=panel_name, style="Header.TLabel").pack(anchor='w', padx=10, pady=5)
        panel_widget.pack(fill=tk.BOTH, expand=True, padx=5)

    def _show_trim_panel(self):
        self._show_panel("Trim Tool", self.trim_frame)

    def _show_adjust_panel(self):
        self._show_panel("Light", self.adjust_frame)

    def _show_color_panel(self):
        self._show_panel("Colour", self.color_frame)

    def _show_filter_panel(self):
        self._show_panel("Filters", self.filter_frame)

    def _create_panel_with_sliders(self, parent, items):
        """A generic function to create a panel containing multiple sliders."""
        frame = ttk.Frame(parent)
        for name, props in items.items():
            row = ttk.Frame(frame)
            row.pack(fill='x', pady=4)
            ttk.Label(row, text=name, width=12).pack(side='left')
            var = tk.DoubleVar(value=props["default"])
            backend_key = props["key"]
            cmd = (lambda val, k=backend_key: self._update_adjustment(k, float(val)))
            scale = ttk.Scale(row, from_=props["range"][0], to=props["range"][1], orient='horizontal', variable=var,
                              command=cmd)
            scale.pack(side='left', fill='x', expand=True, padx=6)
            self.sliders[name] = {"widget": scale, "default": props["default"]}
        return frame

    def _create_trim_panel(self, parent):
        frame = ttk.Frame(parent)
        ttk.Label(frame, text="Start Time (s):").pack(pady=(5, 0))
        self.start_time_entry = ttk.Entry(frame)
        self.start_time_entry.pack(pady=2, padx=10, fill='x')
        ttk.Label(frame, text="End Time (s):").pack(pady=(5, 0))
        self.end_time_entry = ttk.Entry(frame)
        self.end_time_entry.pack(pady=2, padx=10, fill='x')
        ttk.Button(frame, text="Apply Trim", command=self._apply_trim).pack(pady=10)
        return frame

    def _create_adjust_panel(self, parent):
        items = {"Brightness": {"range": (-1.0, 1.0), "default": 0.0, "key": "brightness"},
                 "Contrast": {"range": (-1.0, 1.0), "default": 0.0, "key": "contrast"},
                 "Shadows": {"range": (0.1, 2.0), "default": 1.0, "key": "gamma"},
                 "Highlights": {"range": (0.1, 2.0), "default": 1.0, "key": "gamma"}}
        return self._create_panel_with_sliders(parent, items)

    def _create_color_panel(self, parent):
        items = {"Red": {"range": (0.0, 2.0), "default": 1.0, "key": "r"},
                 "Green": {"range": (0.0, 2.0), "default": 1.0, "key": "g"},
                 "Blue": {"range": (0.0, 2.0), "default": 1.0, "key": "b"}}
        return self._create_panel_with_sliders(parent, items)

    def _create_filter_panel(self, parent):
        frame = ttk.Frame(parent)
        ttk.Button(frame, text="Grayscale", command=lambda: self._apply_filter('grayscale')).pack(pady=10, fill='x',
                                                                                                  padx=10)
        ttk.Button(frame, text="Flip Horizontally", command=lambda: self._apply_filter('mirror_x')).pack(pady=10,
                                                                                                         fill='x',
                                                                                                         padx=10)
        return frame

    # --- Core Functionality ---

    def _load_video(self):
        """Opens a file dialog to load a video and resets the UI."""
        if self.is_playing: self._toggle_playback()
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mov")])
        if file_path and self.processor.load_video(file_path):
            self.status_var.set(f"Loaded: {os.path.basename(file_path)}")
            # IMPORTANT: Reset the sliders in the UI to their default values for the new video.
            self._reset_sliders()
            self._update_preview()
            self._draw_timeline()
        else:
            self.status_var.set("Failed to load video.")

    def _load_audio(self):
        """Opens a file dialog to load an additional audio track."""
        if self.is_playing: self._toggle_playback()
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")])
        if file_path:
            new_audio_count = self.processor.load_audio(file_path)
            if new_audio_count > 0:
                self.status_var.set(f"Added new track: Audio {new_audio_count + 1}")
                self._draw_timeline()
            else:
                self.status_var.set("Failed to load audio.")

    def _export_video(self):
        """Opens a save dialog and exports the final video."""
        if not self.processor.clip:
            messagebox.showwarning("Warning", "Please load a video first.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4 Video", "*.mp4"), ("All Files", "*.*")]
        )

        if file_path:
            self.status_var.set("Exporting... Please wait.")
            self.master.update_idletasks()
            try:
                success = self.processor.export_video(file_path)
                if success:
                    self.status_var.set("Export successful!")
                    messagebox.showinfo(
                        "Export Successful",
                        f"Video was successfully saved to:\n\n{os.path.abspath(file_path)}"
                    )
                else:
                    self.status_var.set("Export failed. Check console for errors.")
                    messagebox.showerror("Export Failed", "Could not export the video.")
            except Exception as e:
                self.status_var.set(f"Export error: {e}")
                messagebox.showerror("Export Error", f"An unexpected error occurred:\n\n{e}")

    def _draw_timeline(self):
        """Draws the video and audio tracks on the timeline canvas."""
        self.timeline_canvas.delete("all")
        self.track_header_canvas.delete("all")
        track_height, ruler_height = 60, 25
        current_y = ruler_height

        # Calculate total duration for the ruler based on the longest clip
        all_clips = []
        if self.processor.clip: all_clips.append(self.processor.clip)
        if self.processor.main_audio_clip: all_clips.append(self.processor.main_audio_clip)
        all_clips.extend(self.processor.additional_audio_clips)
        total_duration = max([c.duration for c in all_clips] + [60]) if all_clips else 60

        # Draw V1 (Video) track
        self.track_header_canvas.create_text(40, current_y + track_height / 2, text="V1", fill=self.TEXT_COLOR,
                                             font=('Segoe UI', 12, 'bold'))
        if self.processor.clip:
            self.timeline_canvas.create_rectangle(0, current_y, self.processor.clip.duration * self.pixels_per_second,
                                                  current_y + track_height, fill=self.ACCENT_COLOR_VIDEO,
                                                  outline="#000")
        current_y += track_height

        # Draw Audio 1 (Main) track
        if self.processor.main_audio_clip:
            self.track_header_canvas.create_text(40, current_y + track_height / 2, text="Audio 1", fill=self.TEXT_COLOR,
                                                 font=('Segoe UI', 10))
            self.timeline_canvas.create_rectangle(0, current_y,
                                                  self.processor.main_audio_clip.duration * self.pixels_per_second,
                                                  current_y + track_height, fill=self.ACCENT_COLOR_AUDIO,
                                                  outline="#000")
            current_y += track_height

        # Draw additional audio tracks
        for i, audio_clip in enumerate(self.processor.additional_audio_clips):
            self.track_header_canvas.create_text(40, current_y + track_height / 2, text=f"Audio {i + 2}",
                                                 fill=self.TEXT_COLOR, font=('Segoe UI', 10))
            self.timeline_canvas.create_rectangle(0, current_y, audio_clip.duration * self.pixels_per_second,
                                                  current_y + track_height, fill=self.ACCENT_COLOR_AUDIO,
                                                  outline="#000")
            current_y += track_height

        # Draw time ruler
        # ... (ruler drawing logic) ...

        self.timeline_canvas.config(scrollregion=(0, 0, total_duration * self.pixels_per_second + 100, current_y + 50))
        self._draw_playhead()

    def _draw_playhead(self):
        """Draws the red line on the timeline indicating the current time."""
        if self.playhead_id: self.timeline_canvas.delete(self.playhead_id)
        x_pos = self.current_time * self.pixels_per_second
        self.playhead_id = self.timeline_canvas.create_line(x_pos, 0, x_pos, 500, fill="red", width=2)

    def _on_timeline_click(self, event):
        """Handles clicks on the timeline to seek to a specific time."""
        if not self.processor.clip: return
        if self.is_playing: self._toggle_playback()
        clicked_x = self.timeline_canvas.canvasx(event.x)
        self.current_time = clicked_x / self.pixels_per_second
        if self.processor.clip and 0 <= self.current_time <= self.processor.clip.duration:
            self.status_var.set(f"Seek to: {self.current_time:.2f}s")
            self._update_preview(time=self.current_time)
            self._draw_playhead()

    def _update_preview(self, time=0):
        """Updates the video preview canvas to show the frame at a specific time."""
        if not self.processor.clip: return
        frame = self.processor.clip.get_frame(time)
        pil_image = Image.fromarray(frame)
        canvas_w, canvas_h = self.preview_canvas.winfo_width(), self.preview_canvas.winfo_height()
        if canvas_w < 2 or canvas_h < 2: return
        ratio = min(canvas_w / self.processor.clip.w, canvas_h / self.processor.clip.h)
        new_size = (int(self.processor.clip.w * ratio), int(self.processor.clip.h * ratio))
        pil_image = pil_image.resize(new_size, Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(image=pil_image)
        self.preview_canvas.delete("all")
        self.preview_canvas.create_image(canvas_w / 2, canvas_h / 2, anchor=tk.CENTER, image=self.tk_image)

    def _resize_preview(self, _event=None):
        """Called when the window is resized to adjust the preview size."""
        self._update_preview(self.current_time)

    def _apply_trim(self):
        """Applies the trim values from the entry boxes."""
        if not self.processor.clip: return
        try:
            start = float(self.start_time_entry.get())
            end = float(self.end_time_entry.get())
            if self.processor.trim_video(start, end):
                self.status_var.set(f"Trimmed from {start}s to {end}s.")
                self._update_preview()
                self._draw_timeline()
                # Clear the entry fields after a successful trim.
                self.start_time_entry.delete(0, tk.END)
                self.end_time_entry.delete(0, tk.END)
            else:
                self.status_var.set("Trim failed.")
        except ValueError:
            self.status_var.set("Error: Invalid time format.")
        except Exception as e:
            self.status_var.set(f"An error occurred: {e}")

    def _update_adjustment(self, key, value):
        """Called when a slider is moved."""
        self.processor.set_adjustment(key, value)
        self.status_var.set(f"{key.capitalize()}: {value:.2f}")
        self._update_preview(self.current_time)

    def _apply_filter(self, filter_name):
        """Called when a filter button is clicked."""
        if not self.processor.clip: return
        self.processor.apply_filter(filter_name)
        self.status_var.set(f"Applied {filter_name} filter.")
        self._update_preview(self.current_time)

    def _reset_all(self):
        """Resets both the backend and the UI to the original state."""
        if self.processor.reset_all_changes():
            self.status_var.set("All changes have been reset.")
            self._reset_sliders()
            self._update_preview()
            self._draw_timeline()
        else:
            self.status_var.set("Load a video first to reset.")

    def _reset_sliders(self):
        """Helper function to set all UI sliders to their default values."""
        for slider_name, slider_info in self.sliders.items():
            slider_info["widget"].set(slider_info["default"])
        print("UI Sliders have been reset.")

    def _toggle_playback(self):
        """Starts or stops video playback."""
        if not self.processor.clip: return
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.play_pause_button.configure(text="⏸ Pause")
            self._playback_loop()
        else:
            self.play_pause_button.configure(text="▶ Play")

    def _playback_loop(self):
        """The main loop that updates the preview during playback."""
        if self.is_playing and self.processor.clip:
            frame_duration = 1 / self.processor.clip.fps
            self.current_time += frame_duration
            if self.current_time >= self.processor.clip.duration:
                self.current_time = self.processor.clip.duration
                self._toggle_playback()
                return
            self._update_preview(self.current_time)
            self._draw_playhead()
            self.master.after(int(frame_duration * 1000), self._playback_loop)


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoEditorUI(root)
    root.mainloop()
