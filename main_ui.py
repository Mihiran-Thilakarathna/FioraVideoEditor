import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from backend_processor import FioraBackend
from PIL import Image, ImageTk
import os


class VideoEditorUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Fiora Super Editor")
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

        self.processor = FioraBackend()
        self.status_var = tk.StringVar(value="Welcome to Fiora Super Editor!")
        self.pixels_per_second = 20
        self.current_time = 0.0
        self.playhead_id = None
        self.icons = {}

        try:
            icon_path = os.path.join("assets", "Fiora.png")
            app_icon = tk.PhotoImage(file=icon_path)
            self.master.iconphoto(False, app_icon)
        except tk.TclError:
            print("Icon not found: Please ensure 'Fiora.png' is in the 'assets' folder.")

        self._load_icons()
        self._create_widgets()

    def _load_icons(self):
        """Loads icons from the assets folder."""
        icon_names = ["import", "export", "trim", "adjust", "filters"]
        for name in icon_names:
            try:
                path = os.path.join("assets", f"{name}_icon.png")
                self.icons[name] = ImageTk.PhotoImage(Image.open(path).resize((20, 20), Image.LANCZOS))
            except FileNotFoundError:
                print(f"Warning: Icon file not found at {path}")
                self.icons[name] = None

    def _create_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", padding=8, relief="flat", background=self.BUTTON_COLOR, foreground=self.TEXT_COLOR,
                        font=('Segoe UI', 10))
        style.map("TButton", background=[('active', '#4c4c4c')])
        style.configure("TFrame", background=self.FRAME_COLOR)
        style.configure("TLabel", background=self.FRAME_COLOR, foreground=self.TEXT_COLOR, font=('Segoe UI', 10))
        style.configure("TScale", background=self.FRAME_COLOR)
        style.configure("Header.TLabel", font=('Segoe UI', 11, 'bold'))

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

        # --- Left Toolbar ---
        ttk.Button(left_frame, text=" Import Video", image=self.icons.get("import"), compound="left",
                   command=self._load_video).pack(fill=tk.X, pady=6, padx=6)
        ttk.Button(left_frame, text=" Import Audio", image=self.icons.get("import"), compound="left",
                   command=self._load_audio).pack(fill=tk.X, pady=6, padx=6)
        ttk.Button(left_frame, text=" Export Video", image=self.icons.get("export"), compound="left",
                   command=self._export_video).pack(fill=tk.X, pady=6, padx=6)
        ttk.Separator(left_frame, orient='horizontal').pack(fill='x', pady=10, padx=5)
        ttk.Label(left_frame, text="Tools").pack()
        ttk.Button(left_frame, text=" Trim", image=self.icons.get("trim"), compound="left",
                   command=self._show_trim_panel).pack(fill=tk.X, pady=6, padx=6)
        ttk.Button(left_frame, text=" Adjust", image=self.icons.get("adjust"), compound="left",
                   command=self._show_adjust_panel).pack(fill=tk.X, pady=6, padx=6)
        ttk.Button(left_frame, text=" Filters", image=self.icons.get("filters"), compound="left",
                   command=self._show_filter_panel).pack(fill=tk.X, pady=6, padx=6)

        # --- Center Panel (Adjusted weights) ---
        preview_container = ttk.Frame(mid_paned)
        mid_paned.add(preview_container, weight=5)
        self.preview_canvas = tk.Canvas(preview_container, bg="black", highlightthickness=0)
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)
        self.preview_canvas.bind("<Configure>", self._resize_preview)
        self.tk_image = None

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

        self._create_trim_panel()
        self._create_adjust_panel()
        self._create_filter_panel()
        self._show_adjust_panel()

        status_bar = tk.Label(self.master, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self._draw_timeline()

    def _clear_right_panel(self):
        for widget in self.right_frame.winfo_children():
            widget.pack_forget()

    def _show_trim_panel(self):
        self._clear_right_panel()
        ttk.Label(self.right_frame, text="Trim Tool", style="Header.TLabel").pack(anchor='w', padx=10, pady=5)
        self.trim_frame.pack(fill=tk.BOTH, expand=True, padx=5)

    def _show_adjust_panel(self):
        self._clear_right_panel()
        ttk.Label(self.right_frame, text="Adjustments", style="Header.TLabel").pack(anchor='w', padx=10, pady=5)
        self.adjust_frame.pack(fill=tk.BOTH, expand=True, padx=5)

    def _show_filter_panel(self):
        self._clear_right_panel()
        ttk.Label(self.right_frame, text="Filters", style="Header.TLabel").pack(anchor='w', padx=10, pady=5)
        self.filter_frame.pack(fill=tk.BOTH, expand=True, padx=5)

    def _create_trim_panel(self):
        self.trim_frame = ttk.Frame(self.right_frame)
        ttk.Label(self.trim_frame, text="Start Time (seconds):").pack(pady=(10, 0))
        self.start_time_entry = ttk.Entry(self.trim_frame)
        self.start_time_entry.pack(pady=5, padx=10, fill='x')
        ttk.Label(self.trim_frame, text="End Time (seconds):").pack(pady=(10, 0))
        self.end_time_entry = ttk.Entry(self.trim_frame)
        self.end_time_entry.pack(pady=5, padx=10, fill='x')
        ttk.Button(self.trim_frame, text="Apply Trim", command=self._apply_trim).pack(pady=20)

    def _create_adjust_panel(self):
        self.adjust_frame = ttk.Frame(self.right_frame)
        self.sliders = {}
        adjust_items = {
            "Brightness": {"range": (-1.0, 1.0), "default": 0.0, "key": "brightness"},
            "Contrast": {"range": (-1.0, 1.0), "default": 0.0, "key": "contrast"},
            "Shadows": {"range": (0.1, 2.0), "default": 1.0, "key": "gamma"},
            "Highlights": {"range": (0.1, 2.0), "default": 1.0, "key": "gamma"}
        }
        for name, props in adjust_items.items():
            frame = ttk.Frame(self.adjust_frame)
            frame.pack(fill='x', pady=4)
            ttk.Label(frame, text=name, width=12).pack(side='left')
            var = tk.DoubleVar(value=props["default"])
            key = props["key"]
            if name == "Highlights":
                command = lambda val, k=key: self._update_adjustment(k, 1.0 / float(val))
            else:
                command = lambda val, k=key: self._update_adjustment(k, float(val))
            scale = ttk.Scale(frame, from_=props["range"][0], to=props["range"][1], orient='horizontal', variable=var,
                              command=command)
            scale.pack(side='left', fill='x', expand=True, padx=6)
            self.sliders[key] = scale

    def _create_filter_panel(self):
        self.filter_frame = ttk.Frame(self.right_frame)
        ttk.Button(self.filter_frame, text="Apply Grayscale", command=self._apply_grayscale).pack(pady=10)

    def _load_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mov")])
        if file_path and self.processor.load_video(file_path):
            self.status_var.set(f"Loaded: {file_path.split('/')[-1]}")
            self._update_preview()
            self._draw_timeline()
        else:
            self.status_var.set("Failed to load video.")

    def _load_audio(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")])
        if file_path and self.processor.load_audio(file_path):
            self.status_var.set("Audio loaded.")
            self._draw_timeline()

    def _export_video(self):
        if not self.processor.clip:
            messagebox.showwarning("Warning", "Please load a video first.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".mp4")
        if file_path:
            self.status_var.set("Exporting...")
            self.master.update()
            if self.processor.export_video(file_path):
                self.status_var.set("Export successful!")
            else:
                self.status_var.set("Export failed.")

    def _draw_timeline(self):
        self.timeline_canvas.delete("all")
        self.track_header_canvas.delete("all")
        track_height, ruler_height, v1_y, audio1_y = 60, 25, 25, 85
        self.track_header_canvas.create_text(40, v1_y + track_height / 2, text="V1", fill=self.TEXT_COLOR,
                                             font=('Segoe UI', 12, 'bold'))
        self.track_header_canvas.create_text(40, audio1_y + track_height / 2, text="Audio 1", fill=self.TEXT_COLOR,
                                             font=('Segoe UI', 10))

        total_duration = 0
        if self.processor.clip: total_duration = max(total_duration, self.processor.clip.duration)
        if self.processor.audio_clip: total_duration = max(total_duration, self.processor.audio_clip.duration)
        if total_duration == 0: total_duration = 60

        if total_duration < 30:
            step = 2
        elif total_duration < 120:
            step = 10
        elif total_duration < 600:
            step = 30
        else:
            step = 60

        def format_time(seconds):
            mins, secs = divmod(int(seconds), 60)
            return f"{mins:02d}:{secs:02d}"

        total_width = (total_duration + step) * self.pixels_per_second
        for i in range(0, int(total_duration) + step, step):
            x_pos = i * self.pixels_per_second
            self.timeline_canvas.create_line(x_pos, 0, x_pos, ruler_height, fill="#666")
            self.timeline_canvas.create_text(x_pos + 5, 5, text=format_time(i), anchor='nw', fill=self.TEXT_COLOR)

        if self.processor.clip:
            clip_width = self.processor.clip.duration * self.pixels_per_second
            self.timeline_canvas.create_rectangle(0, v1_y, clip_width, v1_y + track_height,
                                                  fill=self.ACCENT_COLOR_VIDEO, outline="#000")
        if self.processor.audio_clip:
            clip_width = self.processor.audio_clip.duration * self.pixels_per_second
            self.timeline_canvas.create_rectangle(0, audio1_y, clip_width, audio1_y + track_height,
                                                  fill=self.ACCENT_COLOR_AUDIO, outline="#000")

        self.timeline_canvas.config(scrollregion=(0, 0, total_width, 250))
        self._draw_playhead()

    def _draw_playhead(self):
        if self.playhead_id:
            self.timeline_canvas.delete(self.playhead_id)
        x_pos = self.current_time * self.pixels_per_second
        self.playhead_id = self.timeline_canvas.create_line(x_pos, 0, x_pos, 250, fill="red", width=2)

    def _on_timeline_click(self, event):
        if not self.processor.clip: return
        clicked_x = self.timeline_canvas.canvasx(event.x)
        self.current_time = clicked_x / self.pixels_per_second
        if 0 <= self.current_time <= self.processor.clip.duration:
            self.status_var.set(f"Seek to: {self.current_time:.2f}s")
            self._update_preview(time=self.current_time)
            self._draw_playhead()

    def _update_preview(self, time=0):
        if not self.processor.clip: return
        frame = self.processor.clip.get_frame(time)
        pil_image = Image.fromarray(frame)
        canvas_w, canvas_h = self.preview_canvas.winfo_width(), self.preview_canvas.winfo_height()
        if canvas_w < 2 or canvas_h < 2: return
        img_w, img_h = pil_image.size
        ratio = min(canvas_w / img_w, canvas_h / img_h)
        new_size = (int(img_w * ratio), int(img_h * ratio))
        pil_image = pil_image.resize(new_size, Image.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(image=pil_image)
        self.preview_canvas.delete("all")
        self.preview_canvas.create_image(canvas_w / 2, canvas_h / 2, anchor=tk.CENTER, image=self.tk_image)

    def _resize_preview(self, event=None):
        self._update_preview(self.current_time)

    def _apply_trim(self):
        if not self.processor.clip:
            messagebox.showwarning("Warning", "Please load a video first.")
            return
        try:
            start = float(self.start_time_entry.get())
            end = float(self.end_time_entry.get())
            if self.processor.trim_video(start, end):
                self.status_var.set(f"Trimmed from {start}s to {end}s.")
                self._update_preview()
                self._draw_timeline()
            else:
                self.status_var.set("Trim failed.")
        except ValueError:
            self.status_var.set("Error: Invalid time.")

    def _update_adjustment(self, key, value):
        self.processor.set_adjustment(key, value)
        self.status_var.set(f"{key.capitalize()}: {value:.2f}")
        self._update_preview(self.current_time)

    def _apply_grayscale(self):
        if not self.processor.clip:
            messagebox.showwarning("Warning", "Please load a video first.")
            return
        self.processor.apply_grayscale_filter()
        self.status_var.set("Applied Grayscale filter.")
        self._update_preview(self.current_time)


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoEditorUI(root)
    root.mainloop()