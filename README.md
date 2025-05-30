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
