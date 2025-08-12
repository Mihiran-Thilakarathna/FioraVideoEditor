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

5.  **Run the backend test script:**
    (First, ensure you have changed the placeholder file paths inside the `if __name__ == "__main__":` block in `backend_processor.py`)
    ```bash
    python backend_processor.py
    ```
    
## 🖥️ User Interface

- **Framework:** Tkinter (Python standard library)
- **Layout:** Responsive panes using `ttk.PanedWindow`
- **Features:**
  - Custom window icon (with fallback if missing)
  - Toggleable UI sections for better workflow
  - Intuitive controls for video loading, trimming, and filter application
- **File:** `dashboard_ui.py`## 🖼️ Screenshot

!## 🖼️ Screenshot

![Dashboard UI Screenshot](assets/v01.png)


## 👥 Team Members

* **[T.H.M.Thilakarathna](https://github.com/Mihiran-Thilakarathna)** - *Backend & Project Setup*
* **[D.V.T.R.Vitharana](https://github.com/Thinuka2835)** - *UI/UX Designer*
* **[D.T.P.D Wickramasinghe](https://github.com/Tharinda-Pamindu)** - *Features Developer*
* **[S.H.M.P.K.Senadheera](https://github.com/Piyumanjalee)** - *Features Developer*
* **[D.D.S.S.Kumasaru](https://github.com/Dilakshi13)** - *Documentation & Testing*