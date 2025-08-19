# main_ui.py
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

        self.BG_COLOR = "#2e2e2e";
        self.FRAME_COLOR = "#252628";
        self.BUTTON_COLOR = "#3c3c3c"
        self.TEXT_COLOR = "#ffffff";
        self.ACCENT_COLOR_VIDEO = "#8e44ad";
        self.ACCENT_COLOR_AUDIO_1 = "#27ae60"
        self.ACCENT_COLOR_AUDIO_2 = "#2980b9";
        self.master.configure(bg=self.BG_COLOR)

        self.processor = FioraBackend()
        self.status_var = tk.StringVar(value="Welcome to Fiora Editor!")
        self.pixels_per_second = 20;
        self.current_time = 0.0
        self.playhead_id = None;
        self.icons = {};
        self.sliders = {}
        self.is_playing = False;
        self.tk_image = None

        self.control_widgets = []  # To hold widgets that should be disabled during playback

        try:
            icon_path = os.path.join("assets", "Fiora.png")
            app_icon = tk.PhotoImage(file=icon_path)
            self.master.iconphoto(False, app_icon)
        except tk.TclError:
            print("Icon not found.")

        self._load_icons()
        self._create_widgets()

    def _load_icons(self):
        icon_names = ["import", "export", "trim", "adjust", "filters", "color", "reset", "play", "pause"]
        for name in icon_names:
            try:
                path = os.path.join("assets", f"{name}_icon.png")
                self.icons[name] = ImageTk.PhotoImage(Image.open(path).resize((20, 20), Image.Resampling.LANCZOS))
            except FileNotFoundError:
                self.icons[name] = None

    def _create_widgets(self):
        style = ttk.Style();
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

        self.left_frame = ttk.Frame(main_paned, width=150);
        self.left_frame.pack_propagate(False)
        main_paned.add(self.left_frame)

        import_btn = ttk.Button(self.left_frame, text=" Import Video", image=self.icons.get("import"), compound="left",
                                command=self._load_video)
        import_btn.pack(fill=tk.X, pady=6, padx=6)
        import_audio_btn = ttk.Button(self.left_frame, text=" Import Audio", image=self.icons.get("import"),
                                      compound="left", command=self._load_audio)
        import_audio_btn.pack(fill=tk.X, pady=6, padx=6)
        export_btn = ttk.Button(self.left_frame, text=" Export Video", image=self.icons.get("export"), compound="left",
                                command=self._export_video)
        export_btn.pack(fill=tk.X, pady=6, padx=6)
        ttk.Separator(self.left_frame, orient='horizontal').pack(fill='x', pady=10, padx=5)
        ttk.Label(self.left_frame, text="Tools").pack()
        trim_btn = ttk.Button(self.left_frame, text=" Trim", image=self.icons.get("trim"), compound="left",
                              command=self._show_trim_panel)
        trim_btn.pack(fill=tk.X, pady=6, padx=6)
        light_btn = ttk.Button(self.left_frame, text=" Light", image=self.icons.get("adjust"), compound="left",
                               command=self._show_adjust_panel)
        light_btn.pack(fill=tk.X, pady=6, padx=6)
        color_btn = ttk.Button(self.left_frame, text=" Colour", image=self.icons.get("color"), compound="left",
                               command=self._show_color_panel)
        color_btn.pack(fill=tk.X, pady=6, padx=6)
        filters_btn = ttk.Button(self.left_frame, text=" Filters", image=self.icons.get("filters"), compound="left",
                                 command=self._show_filter_panel)
        filters_btn.pack(fill=tk.X, pady=6, padx=6)

        mid_paned = ttk.Panedwindow(main_paned, orient=tk.VERTICAL);
        main_paned.add(mid_paned, weight=1)
        self.right_frame = ttk.Frame(main_paned, width=300);
        self.right_frame.pack_propagate(False)
        main_paned.add(self.right_frame)
        self.right_content_frame = ttk.Frame(self.right_frame);
        self.right_content_frame.pack(fill=tk.BOTH, expand=True)

        reset_btn = ttk.Button(self.right_frame, text=" Reset All", image=self.icons.get("reset"), compound="left",
                               command=self._reset_all)
        reset_btn.pack(side=tk.BOTTOM, fill=tk.X, pady=10, padx=10)

        self.control_widgets.extend(
            [import_audio_btn, export_btn, trim_btn, light_btn, color_btn, filters_btn, reset_btn])

        preview_container = ttk.Frame(mid_paned);
        mid_paned.add(preview_container, weight=5)
        self.preview_canvas = tk.Canvas(preview_container, bg="black", highlightthickness=0)
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)
        self.preview_canvas.bind("<Configure>", self._resize_preview)

        controls_frame = ttk.Frame(preview_container);
        controls_frame.pack(fill=tk.X, pady=5)
        controls_frame.columnconfigure(0, weight=1)
        self.play_pause_button = ttk.Button(controls_frame, text="▶ Play", command=self._toggle_playback)
        self.play_pause_button.grid(row=0, column=0)

        timeline_panel = ttk.Frame(mid_paned, height=180);
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

        self._create_all_panels()
        self._show_adjust_panel()

        status_bar = tk.Label(self.master, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self._draw_timeline()

    def _set_controls_state(self, state):
        widget_state = 'normal' if state else 'disabled'
        for widget in self.control_widgets:
            widget.config(state=widget_state)
        for panel in [self.trim_frame, self.adjust_frame, self.color_frame, self.filter_frame]:
            for child in panel.winfo_children():
                try:
                    child.config(state=widget_state)
                except tk.TclError:
                    pass

    def _toggle_playback(self):
        if not self.processor.clip: return
        self.is_playing = not self.is_playing

        if self.is_playing:
            self.play_pause_button.config(text="❚❚ Pause")
            self._set_controls_state(False)
            if self.current_time >= self.processor.clip.duration:
                self.current_time = 0.0
            self._playback_loop()
        else:
            self.play_pause_button.config(text="▶ Play")
            self._set_controls_state(True)

    def _playback_loop(self):
        if self.is_playing and self.processor.clip:
            frame_duration = 1 / self.processor.clip.fps
            self.current_time += frame_duration
            if self.current_time >= self.processor.clip.duration:
                self.current_time = 0.0
                self.is_playing = False
                self.play_pause_button.config(text="▶ Play")
                self._set_controls_state(True)
                self._update_preview(self.current_time)
                self._draw_playhead()
                return

            self._update_preview(self.current_time)
            self._draw_playhead()
            self.master.after(int(frame_duration * 1000), self._playback_loop)

    def _on_timeline_click(self, event):
        if not self.processor.clip: return
        if self.is_playing:
            self._toggle_playback()

        clicked_x = self.timeline_canvas.canvasx(event.x)
        self.current_time = max(0, clicked_x / self.pixels_per_second)
        if self.current_time <= self.processor.clip.duration:
            self.status_var.set(f"Seek to: {self.current_time:.2f}s")
            self._update_preview(time=self.current_time)
            self._draw_playhead()

    def _create_all_panels(self):
        self.trim_frame = self._create_trim_panel(self.right_content_frame)
        self.adjust_frame = self._create_adjust_panel(self.right_content_frame)
        self.color_frame = self._create_color_panel(self.right_content_frame)
        self.filter_frame = self._create_filter_panel(self.right_content_frame)

    def _clear_right_panel(self):
        for widget in self.right_content_frame.winfo_children(): widget.pack_forget()

    def _show_panel(self, panel_name, panel_widget):
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
        frame = ttk.Frame(parent)
        for name, props in items.items():
            row = ttk.Frame(frame);
            row.pack(fill='x', pady=4)
            ttk.Label(row, text=name, width=12).pack(side='left')
            var = tk.DoubleVar(value=props["default"]);
            key = props["key"]
            cmd = lambda val, k=key: self._update_adjustment(k, float(val))
            scale = ttk.Scale(row, from_=props["range"][0], to=props["range"][1], orient='horizontal', variable=var,
                              command=cmd)
            scale.pack(side='left', fill='x', expand=True, padx=6)
            self.sliders[key] = scale
        return frame

    def _create_trim_panel(self, parent):
        frame = ttk.Frame(parent)
        ttk.Label(frame, text="Start Time (s):").pack(pady=(5, 0))
        self.start_time_entry = ttk.Entry(frame)
        self.start_time_entry.pack(pady=2, padx=10, fill='x')
        ttk.Label(frame, text="End Time (s):").pack(pady=(5, 0))
        self.end_time_entry = ttk.Entry(frame)
        self.end_time_entry.pack(pady=2, padx=10, fill='x')
        btn = ttk.Button(frame, text="Apply Trim", command=self._apply_trim)
        btn.pack(pady=10)
        self.control_widgets.append(btn)
        return frame

    def _create_adjust_panel(self, parent):
        items = {"Brightness": {"range": (-1.0, 1.0), "default": 0.0, "key": "brightness"},
                 "Contrast": {"range": (-1.0, 1.0), "default": 0.0, "key": "contrast"},
                 "Gamma": {"range": (0.1, 2.0), "default": 1.0, "key": "gamma"}}
        return self._create_panel_with_sliders(parent, items)

    def _create_color_panel(self, parent):
        items = {"Red": {"range": (0.0, 2.0), "default": 1.0, "key": "r"},
                 "Green": {"range": (0.0, 2.0), "default": 1.0, "key": "g"},
                 "Blue": {"range": (0.0, 2.0), "default": 1.0, "key": "b"}}
        return self._create_panel_with_sliders(parent, items)

    def _create_filter_panel(self, parent):
        frame = ttk.Frame(parent)
        gray_btn = ttk.Button(frame, text="Grayscale", command=lambda: self._apply_filter('grayscale'))
        gray_btn.pack(pady=10, fill='x', padx=10)
        flip_btn = ttk.Button(frame, text="Flip Horizontally", command=lambda: self._apply_filter('mirror_x'))
        flip_btn.pack(pady=10, fill='x', padx=10)
        self.control_widgets.extend([gray_btn, flip_btn])
        return frame

    def _load_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mov")])
        if file_path:
            self.current_time = 0.0
            if self.processor.load_video(file_path):
                self.status_var.set(f"Loaded: {os.path.basename(file_path)}")
                self._update_preview();
                self._draw_timeline()
            else:
                self.status_var.set("Failed to load video.")

    def _load_audio(self):
        if self.is_playing: return
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")])
        if file_path and self.processor.load_audio(file_path):
            self.status_var.set("Audio loaded.");
            self._draw_timeline()

    def _export_video(self):
        if not self.processor.clip: messagebox.showwarning("Warning", "Please load a video first."); return
        file_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 Video", "*.mp4")])
        if file_path:
            self.status_var.set("Exporting... This may take a while.");
            self.master.update()
            if self.processor.export_video(file_path):
                messagebox.showinfo("Success", f"Video exported successfully to:\n{file_path}")
                self.status_var.set("Export successful!")
            else:
                messagebox.showerror("Error", "Failed to export video. Check the console for details.")
                self.status_var.set("Export failed.")

    def _draw_timeline(self):
        self.timeline_canvas.delete("all");
        self.track_header_canvas.delete("all")
        track_height, ruler_height, v1_y, a1_y, a2_y = 50, 25, 25, 75, 125
        self.track_header_canvas.create_text(40, v1_y + track_height / 2, text="V1", fill=self.TEXT_COLOR,
                                             font=('Segoe UI', 12, 'bold'))
        self.track_header_canvas.create_text(40, a1_y + track_height / 2, text="Audio 1", fill=self.TEXT_COLOR,
                                             font=('Segoe UI', 10))
        self.track_header_canvas.create_text(40, a2_y + track_height / 2, text="Audio 2", fill=self.TEXT_COLOR,
                                             font=('Segoe UI', 10))
        total_duration = max(self.processor.clip.duration if self.processor.clip else 0, 60)
        step = 1 if total_duration < 10 else 5 if total_duration < 60 else 10

        def format_time(s):
            return f"{int(s // 60):02d}:{int(s % 60):02d}"

        total_width = (total_duration + step) * self.pixels_per_second
        for i in range(0, int(total_duration) + step, step):
            x = i * self.pixels_per_second
            self.timeline_canvas.create_line(x, 0, x, ruler_height, fill="#666")
            self.timeline_canvas.create_text(x + 5, 5, text=format_time(i), anchor='nw', fill=self.TEXT_COLOR)
        if self.processor.clip: self.timeline_canvas.create_rectangle(0, v1_y,
                                                                      self.processor.clip.duration * self.pixels_per_second,
                                                                      v1_y + track_height, fill=self.ACCENT_COLOR_VIDEO,
                                                                      outline="#000")
        if self.processor.video_audio: self.timeline_canvas.create_rectangle(0, a1_y,
                                                                             self.processor.video_audio.duration * self.pixels_per_second,
                                                                             a1_y + track_height,
                                                                             fill=self.ACCENT_COLOR_AUDIO_1,
                                                                             outline="#000")
        if self.processor.external_audio: self.timeline_canvas.create_rectangle(0, a2_y,
                                                                                self.processor.external_audio.duration * self.pixels_per_second,
                                                                                a2_y + track_height,
                                                                                fill=self.ACCENT_COLOR_AUDIO_2,
                                                                                outline="#000")
        self.timeline_canvas.config(scrollregion=(0, 0, total_width, 250))
        self._draw_playhead()

    def _draw_playhead(self):
        if self.playhead_id: self.timeline_canvas.delete(self.playhead_id)
        x_pos = self.current_time * self.pixels_per_second
        self.playhead_id = self.timeline_canvas.create_line(x_pos, 0, x_pos, 250, fill="red", width=2)

    def _update_preview(self, time=0):
        if not self.processor.clip: return
        try:
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
        except Exception as e:
            print(f"Preview update failed: {e}")

    def _resize_preview(self, _event=None):
        self._update_preview(self.current_time)

    def _apply_trim(self):
        if not self.processor.clip: messagebox.showwarning("Warning", "Please load a video first."); return
        try:
            start, end = float(self.start_time_entry.get()), float(self.end_time_entry.get())
            if self.processor.trim_video(start, end):
                self.status_var.set(f"Trimmed from {start}s to {end}s.")
                self.current_time = 0
                self._update_preview();
                self._draw_timeline()
            else:
                self.status_var.set("Trim failed. Check console for details.")
        except ValueError:
            self.status_var.set("Error: Invalid time.")

    def _update_adjustment(self, key, value):
        if self.is_playing: return
        self.processor.set_adjustment(key, value)
        self.status_var.set(f"{key.capitalize()}: {value:.2f}")
        self._update_preview(self.current_time)

    def _apply_filter(self, filter_name):
        if not self.processor.clip: messagebox.showwarning("Warning", "Please load a video first."); return
        self.processor.apply_filter(filter_name)
        self.status_var.set(f"Applied {filter_name} filter.")
        self._update_preview(self.current_time)

    def _reset_all(self):
        if self.processor.reset_all_changes():
            self.status_var.set("All changes have been reset.")
            self._reset_sliders();
            self.current_time = 0.0
            self._update_preview();
            self._draw_timeline()
        else:
            self.status_var.set("Load a video first to reset.")

    def _reset_sliders(self):
        for key, slider in self.sliders.items():
            default_value = 1.0 if key in ["r", "g", "b", "gamma", "speed", "volume"] else 0.0
            slider.set(default_value)
        print("UI Sliders have been reset.")


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoEditorUI(root)
    root.mainloop()
