# FioraVideoEditor 🎬

A simple, modern desktop video editor created for the ICT2210 Mini Project. This application provides core video and audio manipulation functionalities with an intuitive, multi-pane user interface.

## 🌟 Features

- **File Handling:** Import separate video and audio tracks. Export projects as a single MP4 file with audio automatically trimmed to match video length.
- **Interactive Timeline:**
    - Visual, multi-track display for video (`V1`) and audio (`Audio 1`).
    - Dynamic time ruler that adapts to the project's total duration and displays time in `MM:SS` format.
    - Clickable playhead to seek to any point in the video for precise previewing.
    - Horizontal scrolling for long clips.
- **Real-time Preview:** A central preview panel that updates instantly based on timeline seeking and effect adjustments.
- **Editing Tools:**
    - **Trim:** Cut video clips to a specific start and end time via a dedicated properties panel.
    - **Adjustments:** Fine-tune the look of your video with sliders for Brightness, Contrast, Shadows, and Highlights.
    - **Filters:** Apply simple one-click filters like Grayscale.

## 💻 Technology Stack

- **Language:** Python 3.9+
- **Core Logic:** MoviePy (`1.0.3`)
- **Image Processing:** Pillow (for UI preview)
- **User Interface:** Tkinter with `ttk` for a modern look
- **IDE:** PyCharm Community Edition
- **Version Control:** Git & GitHub

## 🚀 Getting Started

To get a local copy up and running, follow these steps exactly.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Mihiran-Thilakarathna/FioraVideoEditor.git](https://github.com/Mihiran-Thilakarathna/FioraVideoEditor.git)
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd FioraVideoEditor
    ```

3.  **Create and activate the virtual environment:**
    ```bash
    # Create the venv
    python -m venv venv

    # Activate the venv on Windows
    .\venv\Scripts\activate
    ```

4.  **Install all required libraries:**
    (This single command installs all necessary packages like `moviepy` and `Pillow` from the `requirements.txt` file.)
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the application:**
    ```bash
    python main_ui.py
    ```
    
## 🖥️ User Interface

The application features a modern, dark-themed, three-pane layout built with Python's native Tkinter library.

* **Left Toolbar:** Provides quick access to main tools (`Trim`, `Adjust`, `Filters`) and file operations (`Import`, `Export`) with icons for a clean look.
* **Center Panel:** A vertically split view with a large, real-time video preview on top and the interactive, multi-track timeline below.
* **Right Properties Panel:** A dynamic panel that displays the relevant controls (sliders, input boxes) for the tool currently selected from the toolbar.

## 👥 Team Members

* **[T.H.M.Thilakarathna](https://github.com/Mihiran-Thilakarathna)** - *Backend & Project Setup*
* **[D.V.T.R.Vitharana](https://github.com/Thinuka2835)** - *UI/UX Designer*
* **[D.T.P.D Wickramasinghe](https://github.com/Tharinda-Pamindu)** - *Features Developer*
* **[S.H.M.P.K.Senadheera](https://github.com/Piyumanjalee)** - *Features Developer*
* **[D.D.S.S.Kumasaru](https://github.com/Dilakshi13)** - *Documentation & Testing*