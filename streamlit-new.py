import streamlit as st
import cv2
import numpy as np
from shapely.geometry import Polygon, box as shapely_box
from ultralytics import YOLO
import tempfile

# Load YOLOv8 model
model = YOLO("yolov5n.pt")

# Define lane polygons
lane_points = {
    "Lane 1": [(184, 531), (409, 111), (460, 105), (485, 529)],
    "Lane 2": [(490, 527), (473, 133), (526, 100), (801, 527)],
}
lane_polygons = {name: Polygon(pts) for name, pts in lane_points.items()}

st.title("🚗 Vehicle Tracking and Lane Counter")
st.markdown(
    """
    **Instructions:**  
    1. Upload a video file (`.mp4`, `.avi`, `.mov`).  
    2. Click **Start Stream** to process and view results.
    """
)

uploaded_file = st.file_uploader("Browse and upload a video", type=["mp4", "avi", "mov"])
frame_placeholder = st.empty()
progress_bar = st.progress(0, text="Waiting to start...")
start_button = st.button("Start Stream")

if uploaded_file is not None and start_button:
    # Reset counters for each run
    lane_counters = {name: 0 for name in lane_points}
    lane_seen_ids = {name: set() for name in lane_points}

    # Save uploaded file to a temporary location
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    video_path = tfile.name

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_idx = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        output = frame.copy()
        results = model.track(frame, persist=True)[0]
        tracks = results.boxes

        if tracks.id is not None:
            ids = tracks.id.cpu().numpy()
            boxes = tracks.xyxy.cpu().numpy()
        else:
            ids = []
            boxes = []

        for tid, box in zip(ids, boxes):
            x1, y1, x2, y2 = map(int, box)
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            bbox_poly = shapely_box(x1, y1, x2, y2)

            for lane_name, polygon in lane_polygons.items():
                if polygon.contains(bbox_poly) and tid not in lane_seen_ids[lane_name]:
                    lane_seen_ids[lane_name].add(tid)
                    lane_counters[lane_name] += 1

            cv2.rectangle(output, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(output, f"ID:{int(tid)}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            cv2.circle(output, (cx, cy), 3, (0, 0, 255), -1)

        # Draw lanes
        for name, pts in lane_points.items():
            overlay = output.copy()
            cv2.fillPoly(overlay, [np.array(pts)], (144, 238, 144))
            cv2.addWeighted(overlay, 0.4, output, 0.6, 0, output)

        # Show counts
        y = 30
        for name in sorted(lane_counters):
            text = f"{name}: {lane_counters[name]}"
            cv2.putText(output, text, (10, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 4)
            cv2.putText(output, text, (10, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            y += 30

        # Convert BGR to RGB
        output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(output, channels="RGB")

        # Update progress bar
        frame_idx += 1
        progress = min(frame_idx / total_frames, 1.0)
        progress_bar.progress(progress, text=f"Processing frame {frame_idx}/{total_frames}")

    cap.release()
    progress_bar.empty()
    st.success("Processing complete!")
    st.write("### Final Lane Counts:")
    for name in sorted(lane_counters):
        st.write(f"**{name}: {lane_counters[name]}**")