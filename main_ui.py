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

        # --- Theme, Colors, and State Variables ---
        self.BG_COLOR = "#2e2e2e";
        self.FRAME_COLOR = "#252628";
        self.BUTTON_COLOR = "#3c3c3c";
        self.TEXT_COLOR = "#ffffff";
        self.ACCENT_COLOR_VIDEO = "#8e44ad";
        self.ACCENT_COLOR_AUDIO = "#27ae60"
        self.master.configure(bg=self.BG_COLOR)

        self.processor = FioraBackend()
        self.status_var = tk.StringVar(value="Welcome to Fiora Editor!")
        self.pixels_per_second = 20;
        self.current_time = 0.0;
        self.playhead_id = None;
        self.icons = {}

        self._load_icons()
        self._create_widgets()

    def _load_icons(self):
        icon_names = ["import", "export", "trim", "adjust", "color", "speed", "filters", "reset"]
        for name in icon_names:
            try:
                path = os.path.join("assets", f"{name}_icon.png")
                self.icons[name] = ImageTk.PhotoImage(Image.open(path).resize((20, 20), Image.LANCZOS))
            except FileNotFoundError:
                self.icons[name] = None

    def _create_widgets(self):
        style = ttk.Style();
        style.theme_use('clam');
        style.configure("TButton", padding=8, relief="flat", background=self.BUTTON_COLOR, foreground=self.TEXT_COLOR,
                        font=('Segoe UI', 10));
        style.map("TButton", background=[('active', '#4c4c4c')]);
        style.configure("TFrame", background=self.FRAME_COLOR);
        style.configure("TLabel", background=self.FRAME_COLOR, foreground=self.TEXT_COLOR, font=('Segoe UI', 10));
        style.configure("TScale", background=self.FRAME_COLOR);
        style.configure("Header.TLabel", font=('Segoe UI', 11, 'bold'))
        main_paned = ttk.Panedwindow(self.master, orient=tk.HORIZONTAL);
        main_paned.pack(fill=tk.BOTH, expand=True, padx=8, pady=(8, 0))
        left_frame = ttk.Frame(main_paned, width=150);
        left_frame.pack_propagate(False);
        main_paned.add(left_frame)
        mid_paned = ttk.Panedwindow(main_paned, orient=tk.VERTICAL);
        main_paned.add(mid_paned, weight=1)
        self.right_frame = ttk.Frame(main_paned, width=300);
        self.right_frame.pack_propagate(False);
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
        ttk.Button(left_frame, text=" Color", image=self.icons.get("color"), compound="left",
                   command=self._show_color_panel).pack(fill=tk.X, pady=6, padx=6)
        ttk.Button(left_frame, text=" Speed", image=self.icons.get("speed"), compound="left",
                   command=self._show_speed_panel).pack(fill=tk.X, pady=6, padx=6)
        ttk.Button(left_frame, text=" Filters", image=self.icons.get("filters"), compound="left",
                   command=self._show_filter_panel).pack(fill=tk.X, pady=6, padx=6)
        ttk.Separator(left_frame, orient='horizontal').pack(fill='x', pady=10, padx=5)
        ttk.Button(left_frame, text=" Reset All", image=self.icons.get("reset"), compound="left",
                   command=self._reset_all).pack(fill=tk.X, pady=6, padx=6)

        # --- Center Panel & Status Bar ---
        preview_container = ttk.Frame(mid_paned);
        mid_paned.add(preview_container, weight=5);
        self.preview_canvas = tk.Canvas(preview_container, bg="black", highlightthickness=0);
        self.preview_canvas.pack(fill=tk.BOTH, expand=True);
        self.preview_canvas.bind("<Configure>", self._resize_preview);
        self.tk_image = None
        timeline_panel = ttk.Frame(mid_paned, height=180);
        mid_paned.add(timeline_panel, weight=1);
        self.track_header_canvas = tk.Canvas(timeline_panel, width=80, bg=self.FRAME_COLOR, highlightthickness=0);
        self.track_header_canvas.pack(side=tk.LEFT, fill=tk.Y);
        h_scroll = ttk.Scrollbar(timeline_panel, orient=tk.HORIZONTAL);
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X);
        self.timeline_canvas = tk.Canvas(timeline_panel, bg="#1e1f23", highlightthickness=0,
                                         xscrollcommand=h_scroll.set);
        self.timeline_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True);
        h_scroll.config(command=self.timeline_canvas.xview);
        self.timeline_canvas.bind("<Button-1>", self._on_timeline_click)

        self._create_all_panels()
        self._show_adjust_panel()  # Show default panel
        status_bar = tk.Label(self.master, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W);
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self._draw_timeline()

    def _create_all_panels(self):
        # Create all panels at startup but keep them hidden
        self.trim_frame = self._create_trim_panel()
        self.adjust_frame = self._create_adjust_panel()
        self.color_frame = self._create_color_panel()
        self.speed_frame = self._create_speed_panel()
        self.filter_frame = self._create_filter_panel()
        self.audio_frame = self._create_audio_panel()

    def _clear_right_panel(self):
        for widget in self.right_frame.winfo_children(): widget.pack_forget()

    def _show_panel(self, panel_name, panel_widget):
        self._clear_right_panel()
        ttk.Label(self.right_frame, text=panel_name, style="Header.TLabel").pack(anchor='w', padx=10, pady=5)
        panel_widget.pack(fill=tk.BOTH, expand=True, padx=5)

    def _show_trim_panel(self):
        self._show_panel("Trim Tool", self.trim_frame)

    def _show_adjust_panel(self):
        self._show_panel("Adjustments", self.adjust_frame)

    def _show_color_panel(self):
        self._show_panel("Color Mixer", self.color_frame)

    def _show_speed_panel(self):
        self._show_panel("Speed Control", self.speed_frame)

    def _show_filter_panel(self):
        self._show_panel("Filters", self.filter_frame)

    def _create_panel_with_sliders(self, parent, items):
        frame = ttk.Frame(parent)
        for name, props in items.items():
            row = ttk.Frame(frame);
            row.pack(fill='x', pady=4)
            ttk.Label(row, text=name, width=12).pack(side='left')
            var = tk.DoubleVar(value=props["default"])
            key = props["key"]
            cmd = (lambda val, k=key: self._update_adjustment(k, 1.0 / float(val))) if name == "Highlights" else (
                lambda val, k=key: self._update_adjustment(k, float(val)))
            scale = ttk.Scale(row, from_=props["range"][0], to=props["range"][1], orient='horizontal', variable=var,
                              command=cmd)
            scale.pack(side='left', fill='x', expand=True, padx=6)
        return frame

    def _create_trim_panel(self):
        frame = ttk.Frame(self.right_frame);
        ttk.Label(frame, text="Start Time (seconds):").pack(pady=(10, 0));
        self.start_time_entry = ttk.Entry(frame);
        self.start_time_entry.pack(pady=5, padx=10, fill='x');
        ttk.Label(frame, text="End Time (seconds):").pack(pady=(10, 0));
        self.end_time_entry = ttk.Entry(frame);
        self.end_time_entry.pack(pady=5, padx=10, fill='x');
        ttk.Button(frame, text="Apply Trim", command=self._apply_trim).pack(pady=20)
        return frame

    def _create_adjust_panel(self):
        items = {"Brightness": {"range": (-1.0, 1.0), "default": 0.0, "key": "brightness"},
                 "Contrast": {"range": (-1.0, 1.0), "default": 0.0, "key": "contrast"},
                 "Shadows": {"range": (0.1, 2.0), "default": 1.0, "key": "gamma"},
                 "Highlights": {"range": (0.1, 2.0), "default": 1.0, "key": "gamma"}}
        return self._create_panel_with_sliders(self.right_frame, items)

    def _create_color_panel(self):
        items = {"Red": {"range": (0.0, 2.0), "default": 1.0, "key": "r"},
                 "Green": {"range": (0.0, 2.0), "default": 1.0, "key": "g"},
                 "Blue": {"range": (0.0, 2.0), "default": 1.0, "key": "b"}}
        return self._create_panel_with_sliders(self.right_frame, items)

    def _create_speed_panel(self):
        items = {"Speed": {"range": (0.25, 4.0), "default": 1.0, "key": "speed"}}
        return self._create_panel_with_sliders(self.right_frame, items)

    def _create_audio_panel(self):  # You can add a button for this if needed
        items = {"Volume": {"range": (0.0, 2.0), "default": 1.0, "key": "volume"}}
        return self._create_panel_with_sliders(self.right_frame, items)

    def _create_filter_panel(self):
        frame = ttk.Frame(self.right_frame)
        ttk.Button(frame, text="Grayscale", command=lambda: self._apply_filter('grayscale')).pack(pady=5, fill='x',
                                                                                                  padx=10)
        ttk.Button(frame, text="Invert Colors", command=lambda: self._apply_filter('invert_colors')).pack(pady=5,
                                                                                                          fill='x',
                                                                                                          padx=10)
        ttk.Button(frame, text="Flip Horizontally", command=lambda: self._apply_filter('mirror_x')).pack(pady=5,
                                                                                                         fill='x',
                                                                                                         padx=10)
        return frame

    def _load_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mov")]);
        if file_path and self.processor.load_video(file_path):
            self.status_var.set(f"Loaded: {os.path.basename(file_path)}"); self._update_preview(); self._draw_timeline()
        else:
            self.status_var.set("Failed to load video.")

    def _load_audio(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")]);
        if file_path and self.processor.load_audio(file_path): self.status_var.set(
            "Audio loaded."); self._draw_timeline()

    def _export_video(self):
        if not self.processor.clip: messagebox.showwarning("Warning", "Please load a video first."); return
        file_path = filedialog.asksaveasfilename(defaultextension=".mp4")
        if file_path:
            self.status_var.set("Exporting...");
            self.master.update()
            if self.processor.export_video(file_path):
                self.status_var.set("Export successful!")
            else:
                self.status_var.set("Export failed.")

    def _draw_timeline(self):
        self.timeline_canvas.delete("all");
        self.track_header_canvas.delete("all")
        track_height, ruler_height, v1_y, audio1_y = 60, 25, 25, 85
        self.track_header_canvas.create_text(40, v1_y + track_height / 2, text="V1", fill=self.TEXT_COLOR,
                                             font=('Segoe UI', 12, 'bold'));
        self.track_header_canvas.create_text(40, audio1_y + track_height / 2, text="Audio 1", fill=self.TEXT_COLOR,
                                             font=('Segoe UI', 10))
        total_duration = max(self.processor.clip.duration if self.processor.clip else 0,
                             self.processor.audio_clip.duration if self.processor.audio_clip else 0, 60)

        if total_duration < 30:
            step = 2
        elif total_duration < 120:
            step = 10
        elif total_duration < 600:
            step = 30
        else:
            step = 60

        def format_time(seconds):
            mins, secs = divmod(int(seconds), 60); return f"{mins:02d}:{secs:02d}"

        total_width = (total_duration + step) * self.pixels_per_second
        for i in range(0, int(total_duration) + step, step):
            x_pos = i * self.pixels_per_second;
            self.timeline_canvas.create_line(x_pos, 0, x_pos, ruler_height, fill="#666");
            self.timeline_canvas.create_text(x_pos + 5, 5, text=format_time(i), anchor='nw', fill=self.TEXT_COLOR)
        if self.processor.clip: self.timeline_canvas.create_rectangle(0, v1_y,
                                                                      self.processor.clip.duration * self.pixels_per_second,
                                                                      v1_y + track_height, fill=self.ACCENT_COLOR_VIDEO,
                                                                      outline="#000")
        if self.processor.audio_clip: self.timeline_canvas.create_rectangle(0, audio1_y,
                                                                            self.processor.audio_clip.duration * self.pixels_per_second,
                                                                            audio1_y + track_height,
                                                                            fill=self.ACCENT_COLOR_AUDIO,
                                                                            outline="#000")
        self.timeline_canvas.config(scrollregion=(0, 0, total_width, 250));
        self._draw_playhead()

    def _draw_playhead(self):
        if self.playhead_id: self.timeline_canvas.delete(self.playhead_id)
        x_pos = self.current_time * self.pixels_per_second;
        self.playhead_id = self.timeline_canvas.create_line(x_pos, 0, x_pos, 250, fill="red", width=2)

    def _on_timeline_click(self, event):
        if not self.processor.clip: return
        clicked_x = self.timeline_canvas.canvasx(event.x);
        self.current_time = clicked_x / self.pixels_per_second
        if 0 <= self.current_time <= self.processor.clip.duration:
            self.status_var.set(f"Seek to: {self.current_time:.2f}s");
            self._update_preview(time=self.current_time);
            self._draw_playhead()

    def _update_preview(self, time=0):
        if not self.processor.clip: return
        frame = self.processor.clip.get_frame(time);
        pil_image = Image.fromarray(frame)
        canvas_w, canvas_h = self.preview_canvas.winfo_width(), self.preview_canvas.winfo_height()
        if canvas_w < 2 or canvas_h < 2: return
        ratio = min(canvas_w / self.processor.clip.w, canvas_h / self.processor.clip.h)
        new_size = (int(self.processor.clip.w * ratio), int(self.processor.clip.h * ratio));
        pil_image = pil_image.resize(new_size, Image.LANCZOS);
        self.tk_image = ImageTk.PhotoImage(image=pil_image);
        self.preview_canvas.delete("all");
        self.preview_canvas.create_image(canvas_w / 2, canvas_h / 2, anchor=tk.CENTER, image=self.tk_image)

    def _resize_preview(self, event=None):
        self._update_preview(self.current_time)

    def _apply_trim(self):
        if not self.processor.clip: messagebox.showwarning("Warning", "Please load a video first."); return
        try:
            start, end = float(self.start_time_entry.get()), float(self.end_time_entry.get())
            if self.processor.trim_video(start, end):
                self.status_var.set(f"Trimmed from {start}s to {end}s."); self._update_preview(); self._draw_timeline()
            else:
                self.status_var.set("Trim failed.")
        except ValueError:
            self.status_var.set("Error: Invalid time.")

    def _update_adjustment(self, key, value):
        self.processor.set_adjustment(key, value);
        self.status_var.set(f"{key.capitalize()}: {value:.2f}");
        self._update_preview(self.current_time)

    def _apply_filter(self, filter_name):
        if not self.processor.clip: messagebox.showwarning("Warning", "Please load a video first."); return
        self.processor.apply_filter(filter_name);
        self.status_var.set(f"Applied {filter_name} filter.");
        self._update_preview(self.current_time)

    def _reset_all(self):
        if self.processor.reset_all_changes():
            self.status_var.set("All changes have been reset.")
            # Reset sliders to default values in the UI as well
            # This part can be made more robust by storing default values
            for panel in [self.adjust_frame, self.color_frame, self.speed_frame, self.audio_frame]:
                for child in panel.winfo_children():
                    if isinstance(child, ttk.Frame):
                        for sub_child in child.winfo_children():
                            if isinstance(sub_child, ttk.Scale):
                                if "gamma" in str(sub_child.cget("command")) or "speed" in str(
                                        sub_child.cget("command")) or "volume" in str(sub_child.cget("command")):
                                    sub_child.set(1.0)
                                else:
                                    sub_child.set(0.0)

            self._update_preview()
            self._draw_timeline()
        else:
            self.status_var.set("Load a video first to reset.")


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoEditorUI(root)
    root.mainloop()