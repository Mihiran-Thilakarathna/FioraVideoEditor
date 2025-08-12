# FioraVideoEditor 🎬

A simple desktop video editor created for the ICT2210 Mini Project. This project is developed by a 5-person team with a focus on core video manipulation functionalities using Python.

## 🌟 Features

- Load video files from the local system.
- Trim videos to a specific start and end time.
- Apply simple visual filters like Grayscale.
- Adjust video properties such as Brightness, Contrast, and Saturation.
- Export the final edited video as a new MP4 file.

## 💻 Technology Stack

- **Language:** Python 3.9+
- **Core Logic:** MoviePy (Version 1.0.3)
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

4.  **Install the required library:**
    *Important Note: We are installing a specific, stable version of MoviePy to avoid a faulty version found on PyPI.*
    ```bash
    pip install moviepy==1.0.3
    ```

5.  **Run the application:**
    ```bash
    python dashboard_ui.py
    ```
    
## 🖥️ User Interface

The application features a modern, dark-themed, three-pane layout built with Python's native Tkinter library, using the `ttk` extension for a contemporary look and feel.

**Key Components:**
* **Main Layout:** A responsive three-pane structure (`ttk.PanedWindow`) consisting of a Toolbar (Left), Main Area (Center), and Properties Panel (Right).
* **Left Toolbar:** Provides quick access to main tools: Cut (`✂️`), Move (`🖱️`), Add Text (`🅰️`), and Adjust (`⚙️`), along with dedicated buttons for `Import` and `Export` operations.
* **Center Panel:** Vertically split into a top section for the video preview with playback controls, and a bottom, scrollable timeline to visualize video clips.
* **Right Properties Panel:** Features collapsible sections for an uncluttered workspace, including:
    * **Adjustments:** Sliders for fine-tuning Brightness, Contrast, Shadows, Highlights, etc.
    * **Color Mixer:** Sliders for individual RGB color correction.
* **Other Elements:** Includes a standard top menu bar (File, Edit, Help) and a status bar at the bottom to display current actions and messages.

## 🖼️ Screenshot

![Fiora Editor UI](assets/ui_screenshot.png)

## 👥 Team Members

* **[T.H.M.Thilakarathna](https://github.com/Mihiran-Thilakarathna)** - *Backend & Project Setup*
* **[D.V.T.R.Vitharana](https://github.com/Thinuka2835)** - *UI/UX Designer*
* **[D.T.P.D Wickramasinghe](https://github.com/Tharinda-Pamindu)** - *Features Developer*
* **[S.H.M.P.K.Senadheera](https://github.com/Piyumanjalee)** - *Features Developer*
* **[D.D.S.S.Kumasaru](https://github.com/Dilakshi13)** - *Documentation & Testing*