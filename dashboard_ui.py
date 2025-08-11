#!/usr/bin/env python3
"""
Modern-looking Tkinter GUI for a simple video editor (placeholder logic only).

Features:
- Dark theme using ttk.Style
- Top menu bar (File, Edit, Help)
- Left toolbar (Cut, Move, Add Text, Adjust, Import, Export) with emoji icons
- Center video preview area (placeholder)
- Bottom timeline (scrollable Canvas with placeholder clip blocks)
- Right properties panel with 2 collapsible sections: Adjustments and Color Mixer
- Sliders for brightness, contrast, shadows, highlights, whites, blacks, levels
- Sliders for Red, Green, Blue in Color Mixer
- Responsive layout using PanedWindow and grid weights
- Placeholder functions for all actions (no actual video processing)
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog


# -------------------------
# Helper / Placeholder logic
# -------------------------
def placeholder_action(action_name):
    """Generic placeholder action — replace with actual logic later."""
    status_var.set(f"Action: {action_name}")
    print(f"[PLACEHOLDER] {action_name}")

# -------------------------
# Tool callbacks
# -------------------------
def select_tool(tool_name):
    global current_tool
    current_tool = tool_name
    # Update toolbar button styles/appearance to show selection
    for name, btn in toolbar_buttons.items():
        if name == tool_name:
            btn.state(['pressed'])
        else:
            btn.state(['!pressed'])
    status_var.set(f"Selected tool: {tool_name}")
    print(f"Selected tool: {tool_name}")

def cut_tool():
    placeholder_action("Cut Tool used")

def move_tool():
    placeholder_action("Move Tool used")

def add_text_tool():
    placeholder_action("Add Text Tool used")

def adjust_tool():
    placeholder_action("Adjust Tool selected")
    select_tool("Adjust")

def import_video():
    filename = filedialog.askopenfilename(
        title="Import Video",
        filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv"), ("All Files", "*.*")]
    )
    if filename:
        placeholder_action(f"Imported video: {filename}")

def export_video():
    filename = filedialog.asksaveasfilename(
        title="Export Video",
        defaultextension=".mp4",
        filetypes=[("MP4 Video", "*.mp4"), ("All Files", "*.*")]
    )
    if filename:
        placeholder_action(f"Exported video to: {filename}")

# -------------------------
# Adjustment callbacks
# -------------------------
def update_adjustment(var_name, *_):
    """Called when an adjustment slider changes."""
    val = adjustments_vars[var_name].get()
    status_var.set(f"{var_name.capitalize()}: {val:.2f}")
    # In a real editor, we'd apply adjustment to preview here
    print(f"[ADJUST] {var_name} = {val:.2f}")

def update_color(var_name, *_):
    """Color mixer slider changed."""
    val = color_vars[var_name].get()
    status_var.set(f"{var_name.upper()}: {int(val)}")
    print(f"[COLOR] {var_name.upper()} = {int(val)}")

# -------------------------
# Collapsible sections utils
# -------------------------
def toggle_frame(frame_container, toggle_btn):
    """Toggle visibility of a frame inside a container (pack/grid aware)."""
    if frame_container.winfo_viewable():
        frame_container.forget()
        toggle_btn.configure(text="► " + toggle_btn.original_text)
    else:
        frame_container.pack(fill="x", padx=6, pady=(0,6))
        toggle_btn.configure(text="▼ " + toggle_btn.original_text)

# -------------------------
# Build main application
# -------------------------
root = tk.Tk()
root.title("Fiora Editor")
root.geometry("1200x750")
root.minsize(900, 600)
root.iconbitmap("icon.ico")


# -------------------------
# Dark theme styling
# -------------------------
style = ttk.Style(root)
style.theme_use('clam')  # 'clam' is easier to customize for dark mode

DARK_BG = "#1e1f23"
DARK_PANEL = "#252628"
DARK_ACCENT = "#2b8cff"
TEXT_COLOR = "#e6eef6"
SUBTEXT = "#9aa6b2"

root.configure(bg=DARK_BG)
style.configure('.', background=DARK_BG, foreground=TEXT_COLOR, font=('Segoe UI', 10))
style.configure('TFrame', background=DARK_PANEL)
style.configure('TLabel', background=DARK_PANEL, foreground=TEXT_COLOR)
style.configure('TButton', relief='flat', padding=6)
style.map('TButton', background=[('active', '#333438')])
style.configure('Tool.TButton', background=DARK_PANEL, foreground=TEXT_COLOR)
style.configure('TLabelFrame', background=DARK_PANEL, foreground=TEXT_COLOR)
style.configure('TScale', background=DARK_PANEL)
style.configure('Status.TLabel', background=DARK_BG, foreground=SUBTEXT)

# -------------------------
# Top menu bar
# -------------------------
menubar = tk.Menu(root, tearoff=False)
file_menu = tk.Menu(menubar, tearoff=False)
file_menu.add_command(label="New Project", command=lambda: placeholder_action("New Project"))
file_menu.add_command(label="Open...", command=lambda: placeholder_action("Open Project"))
file_menu.add_command(label="Save", command=lambda: placeholder_action("Save Project"))
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=file_menu)

edit_menu = tk.Menu(menubar, tearoff=False)
edit_menu.add_command(label="Undo", command=lambda: placeholder_action("Undo"))
edit_menu.add_command(label="Redo", command=lambda: placeholder_action("Redo"))
menubar.add_cascade(label="Edit", menu=edit_menu)

help_menu = tk.Menu(menubar, tearoff=False)
help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "MiniVideo — Prototype\nTkinter Video Editor GUI"))
menubar.add_cascade(label="Help", menu=help_menu)
root.config(menu=menubar)

# -------------------------
# Paned layout: left | center+bottom | right
# -------------------------
main_paned = ttk.Panedwindow(root, orient=tk.HORIZONTAL)
main_paned.pack(fill=tk.BOTH, expand=True, padx=8, pady=(8,0))

# Left toolbar frame
left_frame = ttk.Frame(main_paned, width=80)
left_frame.pack_propagate(False)  # keep width
main_paned.add(left_frame, weight=0)

# Middle pane will itself be a vertical paned window (preview above, timeline below)
mid_paned = ttk.Panedwindow(main_paned, orient=tk.VERTICAL)
main_paned.add(mid_paned, weight=3)

# Right properties frame
right_frame = ttk.Frame(main_paned, width=320)
right_frame.pack_propagate(False)
main_paned.add(right_frame, weight=1)

# -------------------------
# Left toolbar (emoji icons + Import/Export)
# -------------------------
toolbar_label = ttk.Label(left_frame, text="TOOLS", anchor="center", font=('Segoe UI', 9, 'bold'))
toolbar_label.pack(fill='x', pady=(6,4))

toolbar_buttons = {}
current_tool = None

def make_toolbar_button(parent, name, emoji, command):
    btn = ttk.Button(parent, text=f"{emoji}\n{name}", style='Tool.TButton', command=lambda: [command(), select_tool(name)])
    btn.pack(fill='x', pady=6, padx=6)
    toolbar_buttons[name] = btn
    return btn

# Tools
make_toolbar_button(left_frame, "Cut", "✂️", cut_tool)
make_toolbar_button(left_frame, "Move", "🖱️", move_tool)
make_toolbar_button(left_frame, "Add Text", "🅰️", add_text_tool)
make_toolbar_button(left_frame, "Adjust", "⚙️", adjust_tool)
# Import/Export buttons (these don’t select tools)
imp_btn = ttk.Button(left_frame, text="📁\nImport", style='Tool.TButton', command=import_video)
imp_btn.pack(fill='x', pady=6, padx=6)
exp_btn = ttk.Button(left_frame, text="💾\nExport", style='Tool.TButton', command=export_video)
exp_btn.pack(fill='x', pady=6, padx=6)

# -------------------------
# Middle top: Video preview
# -------------------------
preview_container = ttk.Frame(mid_paned)
mid_paned.add(preview_container, weight=3)

preview_label = ttk.Label(preview_container, text="Preview", font=('Segoe UI', 11, 'bold'))
preview_label.pack(anchor='nw', padx=6, pady=(6,0))

preview_canvas = tk.Canvas(preview_container, bg="#0f1113", highlightthickness=0)
preview_canvas.pack(fill='both', expand=True, padx=6, pady=6)

def draw_preview_placeholder(event=None):
    preview_canvas.delete("all")
    w = preview_canvas.winfo_width()
    h = preview_canvas.winfo_height()
    preview_canvas.create_rectangle(10, 10, w-10, h-10, outline="#2e2f33", width=2)
    preview_canvas.create_text(w//2, h//2, text="Video Preview\n(placeholder)", fill=SUBTEXT, font=('Segoe UI', 14), justify='center')
preview_canvas.bind("<Configure>", draw_preview_placeholder)

controls_frame = ttk.Frame(preview_container)
controls_frame.pack(fill='x', padx=6, pady=(0,6))

ttk.Button(controls_frame, text="⏮️ Prev", command=lambda: placeholder_action("Prev Frame")).pack(side='left', padx=(0,6))
ttk.Button(controls_frame, text="⏯️ Play/Pause", command=lambda: placeholder_action("Play/Pause")).pack(side='left', padx=6)
ttk.Button(controls_frame, text="⏭️ Next", command=lambda: placeholder_action("Next Frame")).pack(side='left', padx=6)

# -------------------------
# Middle bottom: Timeline (scrollable)
# -------------------------
timeline_container = ttk.Frame(mid_paned)
mid_paned.add(timeline_container, weight=1)

timeline_label = ttk.Label(timeline_container, text="Timeline", font=('Segoe UI', 10, 'bold'))
timeline_label.pack(anchor='nw', padx=6, pady=(6,0))

timeline_canvas_frame = ttk.Frame(timeline_container)
timeline_canvas_frame.pack(fill='both', expand=True, padx=6, pady=6)

h_scroll = ttk.Scrollbar(timeline_canvas_frame, orient=tk.HORIZONTAL)
h_scroll.pack(side='bottom', fill='x')

timeline_canvas = tk.Canvas(timeline_canvas_frame, height=140, bg="#141517", highlightthickness=0, xscrollcommand=h_scroll.set)
timeline_canvas.pack(side='left', fill='both', expand=True)
h_scroll.config(command=timeline_canvas.xview)

timeline_inner = ttk.Frame(timeline_canvas)
timeline_window = timeline_canvas.create_window((0,0), window=timeline_inner, anchor='nw')

def populate_timeline():
    for i in range(12):
        block = ttk.Frame(timeline_inner, width=180, height=90, style='TFrame')
        block.grid(row=0, column=i, padx=6, pady=12)
        block.pack_propagate(False)
        lbl = ttk.Label(block, text=f"Clip {i+1}\n00:0{i}:00", anchor='center')
        lbl.pack(expand=True)
    timeline_inner.update_idletasks()
    timeline_canvas.configure(scrollregion=timeline_canvas.bbox("all"))

populate_timeline()

def resize_timeline_canvas(event):
    timeline_canvas.itemconfig(timeline_window, height=timeline_canvas.winfo_height())
    timeline_canvas.configure(scrollregion=timeline_canvas.bbox("all"))

timeline_canvas.bind("<Configure>", resize_timeline_canvas)

# -------------------------
# Right: Properties panel with collapsible sections
# -------------------------
prop_label = ttk.Label(right_frame, text="Properties", font=('Segoe UI', 11, 'bold'))
prop_label.pack(anchor='nw', padx=6, pady=(6,4))

prop_scroll_canvas = tk.Canvas(right_frame, bg=DARK_PANEL, highlightthickness=0)
prop_scroll_canvas.pack(fill='both', expand=True, padx=6, pady=(0,6))

prop_scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=prop_scroll_canvas.yview)
prop_scrollbar.pack(side='right', fill='y')
prop_scroll_canvas.configure(yscrollcommand=prop_scrollbar.set)

prop_inner = ttk.Frame(prop_scroll_canvas)
prop_window = prop_scroll_canvas.create_window((0,0), window=prop_inner, anchor='nw', width=300)

def on_prop_configure(event):
    prop_scroll_canvas.configure(scrollregion=prop_scroll_canvas.bbox("all"))
prop_inner.bind("<Configure>", on_prop_configure)

# Adjustments collapsible section
adjust_header = ttk.Frame(prop_inner)
adjust_header.pack(fill='x', pady=(6,2))
adjust_toggle = ttk.Button(adjust_header, text="▼ Adjustments", style='Tool.TButton')
adjust_toggle.original_text = "Adjustments"
adjust_toggle.pack(side='left', anchor='w')

adjust_frame = ttk.Frame(prop_inner, relief='flat')
adjust_frame.pack(fill='x', padx=6, pady=(0,6))

adjustment_names = ["brightness", "contrast", "shadows", "highlights", "whites", "blacks", "levels"]
adjustments_vars = {}
for name in adjustment_names:
    frame = ttk.Frame(adjust_frame)
    frame.pack(fill='x', pady=4)
    lbl = ttk.Label(frame, text=name.capitalize(), width=12)
    lbl.pack(side='left')
    var = tk.DoubleVar(value=0.0 if name != "levels" else 1.0)
    adjustments_vars[name] = var
    scale = ttk.Scale(frame, from_=-100, to=100, orient='horizontal', variable=var,
                      command=lambda val, n=name: update_adjustment(n))
    scale.pack(side='left', fill='x', expand=True, padx=6)
    val_lbl = ttk.Label(frame, textvariable=tk.StringVar(value=str(var.get())), width=6)
    def make_updater(v, dest_label):
        def updater(*_):
            dest_label.configure(text=f"{v.get():.2f}")
        return updater
    var.trace_add('write', make_updater(var, val_lbl))
    val_lbl.pack(side='right')

adjust_toggle.configure(command=lambda: toggle_frame(adjust_frame, adjust_toggle))

# Color Mixer collapsible section
color_header = ttk.Frame(prop_inner)
color_header.pack(fill='x', pady=(4,2))
color_toggle = ttk.Button(color_header, text="▼ Color Mixer", style='Tool.TButton')
color_toggle.original_text = "Color Mixer"
color_toggle.pack(side='left', anchor='w')

color_frame = ttk.Frame(prop_inner, relief='flat')
color_frame.pack(fill='x', padx=6, pady=(0,6))

color_vars = {}
for name in ['r', 'g', 'b']:
    frame = ttk.Frame(color_frame)
    frame.pack(fill='x', pady=4)
    lbl = ttk.Label(frame, text=name.upper(), width=3)
    lbl.pack(side='left')
    var = tk.IntVar(value=128)
    color_vars[name] = var
    scale = ttk.Scale(frame, from_=0, to=255, orient='horizontal', variable=var,
                      command=lambda val, n=name: update_color(n))
    scale.pack(side='left', fill='x', expand=True, padx=6)
    val_lbl = ttk.Label(frame, textvariable=tk.StringVar(value=str(var.get())), width=4)
    def make_color_updater(v, dest_label):
        def updater(*_):
            dest_label.configure(text=f"{v.get()}")
        return updater
    var.trace_add('write', make_color_updater(var, val_lbl))
    val_lbl.pack(side='right')

color_toggle.configure(command=lambda: toggle_frame(color_frame, color_toggle))

# -------------------------
# Status bar
# -------------------------
status_var = tk.StringVar(value="Ready")
status_bar = ttk.Label(root, textvariable=status_var, style='Status.TLabel', anchor='w', padding=(8,4))
status_bar.pack(side='bottom', fill='x')

# Call select_tool AFTER status_var is created to avoid errors
select_tool("Move")

# -------------------------
# Responsive resizing behavior
# -------------------------
root.update_idletasks()
for i in range(3):
    root.grid_rowconfigure(i, weight=1)
for i in range(3):
    root.grid_columnconfigure(i, weight=1)

# -------------------------
# Keyboard shortcuts
# -------------------------
root.bind('<Control-q>', lambda e: root.quit())
root.bind('<Control-s>', lambda e: placeholder_action("Save Project"))

# -------------------------
# Run the application
# -------------------------
if __name__ == "__main__":
    root.mainloop()
