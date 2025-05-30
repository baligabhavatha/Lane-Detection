# Lane-wise Vehicle Counting

A Streamlit-based application for detecting and counting vehicles in predefined lanes using YOLOv8 for object detection and tracking. The application processes uploaded videos, draws bounding boxes around detected vehicles, tracks them across lanes, and displays lane-wise vehicle counts in real-time or as a downloadable processed video.

## Features
- **Vehicle Detection and Tracking**: Uses YOLOv8 (`yolov8n.pt`) for detecting and tracking vehicles in videos.
- **Lane-wise Counting**: Counts unique vehicles in predefined lanes using Shapely for polygon-based detection.
- **Real-time Visualization**: Streamlit interface (`streamlit-new.py`) for live video processing and display.
- **Video Output**: Processes videos and saves output with annotations (`saveVideo.py`).
- **Docker Support**: Containerized setup for easy deployment.

## Prerequisites
- Python 3.8 or higher
- FFmpeg (for video encoding)
- Docker (optional, for containerized deployment)
- A compatible video file (`.mp4`, `.avi`, or `.mov`)

## Installation

### Local Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/<your-username>/Lane-Detection.git
   cd Lane-Detection
   ```
 2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
 3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
```
 4. **Install FFmpeg**:
    
   Ubuntu
   ```bash
   sudo apt update
   sudo apt install ffmpeg   
```
   macOS:
   ```bash
   brew install ffmpeg
   Windows:
   Download from FFmpeg Website and add to your system PATH.
```
 5. **Download YOLOv8 Model**

The code uses `yolov8n.pt`. You can either:

- Download it manually from the [Ultralytics YOLOv8 repository](https://github.com/ultralytics/ultralytics), **or**
- Allow the `ultralytics` library to automatically download it the first time you run the application.

6. **Run the Application**

You can now run either of the Streamlit applications:

#### Real-time Visualization (`streamlit-new.py`)

```bash
streamlit run streamlit-new.py
```
7. **Configure Lane Polygons** (Optional)

Lane regions are defined using polygon coordinates. These are **hardcoded** in both `process_video.py` and `streamlit-new.py` under the variable `lane_points`.

To customize lanes for your specific video layout:

1. Open either `process_video.py` or `streamlit-new.py`.
2. Locate the `lane_points` definition.
3. Modify the list of coordinates to match your lanes.

Example format:

```python
lane_points = [
    [(100, 300), (200, 300), (200, 500), (100, 500)],  # Lane 1
    [(210, 300), (310, 300), (310, 500), (210, 500)],  # Lane 2
    ...
]
```
8. **Ensure Model Consistency**

Ensure that **all scripts use the same YOLOv8 model** (`yolov8n.pt`) to maintain consistent results across the application.

By default:
- `process_video.py` uses `yolov8n.pt`
- `streamlit-new.py` may use `yolov5n.pt` (older version)

#### ✅ Fix:

Open `streamlit-new.py` and replace the model loading line with:

```python
from ultralytics import YOLO
model = YOLO("yolov8n.pt")

```

### 9. Manage Temporary Files

During video processing, the application generates temporary files such as `temp_output.mp4`.

#### Recommendations:

- **Disk Space**: Ensure you have enough disk space to handle temporary and output files.
- **Auto-cleanup (Optional)**: You can manually or programmatically delete temporary files after processing to free up space.

Example cleanup snippet (Python):

```python
import os
if os.path.exists("temp_output.mp4"):
    os.remove("temp_output.mp4")
```
10. **Streamlit Limitations**

Some video formats may not preview properly within the Streamlit interface due to codec or format compatibility issues.

#### Tips:

- Use standard formats like `.mp4` with H.264 encoding for best compatibility.
- If preview fails:
  - Try re-encoding the video using FFmpeg:

    ```bash
    ffmpeg -i input.avi -vcodec libx264 -crf 23 output.mp4
    ```
  - Or download the processed video directly and view it locally.

> ℹ️ This limitation is specific to Streamlit’s `st.video()` component and not a bug in the processing logic.


11. **Customize Processing Duration**

By default, the application only processes the **first 15 seconds** of any uploaded video to ensure faster performance and quick previews.

#### To change this limit:

1. Open `process_video.py`
2. Locate the configuration variable:

```python
duration_sec = 15
```
Modify it to your desired duration (in seconds), for example: duration_sec = 60

⏱️ Note: Longer durations may increase processing time and memory usage significantly.
---

**a.** Want help turning `duration_sec` into a Streamlit slider or input field for dynamic control?  
**b.** Should we add command-line argument support to control duration when running as a script?
---

12. **Troubleshooting**

Common issues and recommended fixes:

#### ✅ YOLO model not found or not downloading
- Ensure `ultralytics` is installed correctly:
  ```bash
  pip install ultralytics==8.1.22

---

## 🐳 Optional: Docker Setup

You can run the entire application in a Docker container for a consistent and portable environment.

### 1. Build the Docker Image

```bash
docker build -t lane-detection .
```
### 2. Run rhe Docker container
``` bash
docker run -p 8595:8595 lane-detection
```

---

## 🤝 Contributing

We welcome contributions to improve lane detection, tracking, UI/UX, or documentation.

### How to Contribute

1. **Fork** the repository
2. **Create a branch** for your feature or bugfix:
   ```bash
   git checkout -b feature-name
   ```
3. **Push to your fork**
```bash
git push origin feature-name
```
4. **Open a Pull Request with a detailed description of your changes.**

---

## 📜 License

This project is licensed under the **MIT License**.

You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, under the following conditions:

- You must include the original copyright
- The license and permission notice must be included in all copies or substantial portions of the Software

THE SOFTWARE IS PROVIDED **"AS IS"**, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

See the full [LICENSE](./LICENSE) file for details.


---

## 📝 Contributor Agreement

By contributing to this repository, you agree that:

1. You have authored the code or have permission to contribute it.
2. You grant the project maintainers the right to use, modify, and distribute your contributions as part of this project under the MIT License.
3. You understand your contributions will be publicly available under the same license as the project.

> For larger contributions or feature changes, please consider opening an issue first to discuss your idea before submitting a pull request.
