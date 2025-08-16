Of course, here is a more detailed, industry-standard README file for your project.

-----

# Fiora Video Editor

[](https://www.python.org/downloads/)
[](https://opensource.org/licenses/MIT)

A simple and modern desktop video editor built with Python, Tkinter, and MoviePy. Fiora provides core video and audio manipulation functionalities through an intuitive, multi-pane user interface, making it easy to perform essential editing tasks.

*(Suggestion: Replace this with a screenshot or GIF of your application)*

## Features

Fiora Video Editor comes packed with features designed for an efficient editing workflow:

  * **🎬 File Handling**:

      * Import separate video (`.mp4`, `.avi`, `.mov`) and audio (`.mp3`, `.wav`, `.ogg`) tracks.
      * Export projects into a single, combined MP4 file.
      * Audio tracks are automatically trimmed or extended to match the video's final duration.

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
      * **Adjustments**: Fine-tune the look of your video with real-time sliders for:
          * Brightness
          * Contrast
          * Shadows (Gamma)
          * Highlights
      * **Filters**: Apply simple one-click filters, such as Grayscale, to alter the mood of your video.

## Technology Stack

This project leverages a combination of powerful and standard Python libraries:

  * **Core Logic**: [**MoviePy**](https://zulko.github.io/moviepy/) for all video and audio processing tasks.
  * **User Interface**: [**Tkinter**](https://docs.python.org/3/library/tkinter.html) (with the `ttk` extension) for creating the native desktop GUI.
  * **Image Processing**: [**Pillow (PIL)**](https://www.google.com/search?q=https://python-pillow.org/) for handling image conversions for the video preview panel.
  * **Language**: **Python 3.9+**
  * **IDE**: PyCharm Community Edition
  * **Version Control**: Git & GitHub

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

Ensure you have Python 3.9 or higher installed on your system.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Mihiran-Thilakarathna/FioraVideoEditor.git
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd FioraVideoEditor
    ```
3.  **Create and activate a virtual environment:**
    ```bash
    # Create the virtual environment
    python -m venv venv

    # Activate on Windows
    .\venv\Scripts\activate

    # Activate on macOS/Linux
    source venv/bin/activate
    ```
4.  **Install the required libraries:**
    The `requirements.txt` file is not present in the provided files, but based on the code, you would need to create one with `moviepy` and `Pillow`. For now, you can install them directly:
    ```bash
    pip install moviepy Pillow
    ```
5.  **Run the application:**
    ```bash
    python main_ui.py
    ```

## Project Structure

```
FioraVideoEditor/
├── assets/
│   ├── adjust_icon.png
│   ├── export_icon.png
│   ├── filters_icon.png
│   ├── import_icon.png
│   └── trim_icon.png
├── .gitignore
├── backend_processor.py  # Handles all video/audio processing with MoviePy
├── main_ui.py            # Main application entry point and Tkinter UI code
└── README.md
```

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information. (Note: You'll need to add a LICENSE file with the MIT license text).

## Authors

* **[T.H.M.Thilakarathna](https://github.com/Mihiran-Thilakarathna)** - *Backend & Project Setup*
* **[D.V.T.R.Vitharana](https://github.com/Thinuka2835)** - *UI/UX Designer*
* **[D.T.P.D Wickramasinghe](https://github.com/Tharinda-Pamindu)** - *Features Developer*
* **[S.H.M.P.K.Senadheera](https://github.com/Piyumanjalee)** - *Features Developer*
* **[D.D.S.S.Kumasaru](https://github.com/Dilakshi13)** - *Documentation & Testing*