# FioraVideoEditor 🎬

A simple, modern desktop video editor created for the ICT2210 Mini Project. This application provides a comprehensive set of core video and audio manipulation functionalities through an intuitive, multi-pane user interface.

## 🌟 Features

Fiora Video Editor comes packed with features designed for an efficient editing workflow:

* **🎬 File Handling**:
    * Import separate video (`.mp4`, `.avi`, `.mov`) and audio (`.mp3`, `.wav`, `.ogg`) tracks.
    * Export projects into a single, combined MP4 file.
    * Audio tracks are automatically trimmed to match the video's final duration.

* **🎞️ Interactive Timeline**:
    * A visual, multi-track display for video (`V1`) and audio (`Audio 1`).
    * Dynamic time ruler that intelligently adapts its markers to the project's total duration, displaying time in a clear `MM:SS` format.
    * A clickable playhead allows you to instantly seek to any point in the video for precise previewing.
    * Supports horizontal scrolling to easily navigate longer video clips.

* **🖥️ Real-time Preview**:
    * A central preview panel that updates instantly based on timeline seeking and any applied adjustments or filters.
    * The preview window intelligently resizes the video to fit the available space while maintaining the correct aspect ratio.

* **🛠️ Editing Tools**:
    * **Trim**: Easily cut video clips to a specific start and end time using a dedicated properties panel.
    * **Light Adjust**: Fine-tune the look of your video with real-time sliders for:
        * Brightness
        * Contrast
        * Shadows
        * Highlights
    * **Colour Adjust (RGB Mixer)**: Independently control the Red, Green, and Blue color channels using dedicated sliders.
    * **Filters**: Apply simple one-click filters to alter the mood of your video, including:
        * Grayscale
        * Flip Horizontally
    * **Reset**: A dedicated "Reset All" button to instantly revert all edits and adjustments back to the original state of the loaded video.

## 📁 Project Structure

The project is organized into a clean and understandable structure:


FioraVideoEditor/
├── assets/
│   ├── Fiora.png
│   ├── adjust_icon.png
│   ├── color_icon.png
│   ├── export_icon.png
│   ├── filters_icon.png
│   ├── import_icon.png
│   ├── reset_icon.png
│   └── trim_icon.png
├── .gitignore
├── backend_processor.py
├── main_ui.py
├── README.md
└── requirements.txt


* **`assets/`**: Contains all static assets, such as UI icons and the main application icon.
* **`.gitignore`**: Specifies which files and folders (like `venv/` and `.idea/`) should be ignored by Git.
* **`backend_processor.py`**: The core engine of the application. This file contains the `FioraBackend` class, which handles all video and audio processing logic using the MoviePy library.
* **`main_ui.py`**: The main entry point for the application. It contains the `VideoEditorUI` class, which builds and manages the entire graphical user interface using Tkinter.
* **`README.md`**: This file, providing documentation for the project.
* **`requirements.txt`**: Lists all the Python libraries required to run the project, ensuring a consistent setup for all developers.

## 💻 Technology Stack

- **Language:** Python 3.9+
- **Core Logic:** MoviePy (`1.0.3`)
- **Image Processing:** Pillow, NumPy
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
    (This single command installs all necessary packages like `moviepy`, `Pillow`, and `numpy` from the `requirements.txt` file.)
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the application:**
    ```bash
    python main_ui.py
    ```
    
## 🖥️ User Interface

The application features a modern, dark-themed, three-pane layout:

* **Left Toolbar:** Provides quick access to file operations (`Import`, `Export`) and all major editing tools (`Trim`, `Light`, `Colour`, `Filters`).
* **Center Panel:** A vertically split view with a large, real-time video preview on top and the interactive, multi-track timeline below.
* **Right Properties Panel:** A dynamic panel that displays the relevant controls (sliders, input boxes) for the tool currently selected from the toolbar. A dedicated `Reset All` button is located at the bottom for easy access.

## 👥 Team Members

* **[T.H.M.Thilakarathna](https://github.com/Mihiran-Thilakarathna)** - *Backend & Project Setup*
* **[D.V.T.R.Vitharana](https://github.com/Thinuka2835)** - *UI/UX Designer*
* **[D.T.P.D Wickramasinghe](https://github.com/Tharinda-Pamindu)** - *Features Developer*
* **[S.H.M.P.K.Senadheera](https://github.com/Piyumanjalee)** - *Features Developer*
* **[D.D.S.S.Kumasaru](https://github.com/Dilakshi13)** - *Documentation & Testing*

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information. (Note: You'll need to add a LICENSE file with the MIT license text).
