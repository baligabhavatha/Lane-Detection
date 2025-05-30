import cv2
import numpy as np
from shapely.geometry import Polygon, box as shapely_box
from ultralytics import YOLO
import subprocess
import os

def convert_to_h264(input_path, output_path):
    command = [
        'ffmpeg', '-y', '-i', input_path,
        '-c:v', 'libx264', '-preset', 'ultrafast',
        '-pix_fmt', 'yuv420p',
        '-movflags', '+faststart',
        output_path
    ]
    subprocess.run(command, check=True)

def run_yolo_processing(input_path, output_path, duration_sec=15):
    model = YOLO("yolov8n.pt")

    lane_points = {
        "Lane 1": [(184, 531), (409, 111), (460, 105), (485, 529)],
        "Lane 2": [(490, 527), (473, 133), (526, 100), (801, 527)],
    }
    lane_polygons = {name: Polygon(pts) for name, pts in lane_points.items()}

    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(min(cap.get(cv2.CAP_PROP_FRAME_COUNT), duration_sec * fps))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    temp_output = "temp_output.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Temporary output with basic codec
    out = cv2.VideoWriter(temp_output, fourcc, fps, (width, height))

    lane_counters = {name: 0 for name in lane_points}
    lane_seen_ids = {name: set() for name in lane_points}

    frame_idx = 0
    while cap.isOpened() and frame_idx < total_frames:
        ret, frame = cap.read()
        if not ret:
            break

        output = frame.copy()
        results = model.track(frame, persist=True)[0]
        tracks = results.boxes

        ids = tracks.id.cpu().numpy() if tracks.id is not None else []
        boxes = tracks.xyxy.cpu().numpy() if tracks.id is not None else []

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

        for name, pts in lane_points.items():
            overlay = output.copy()
            cv2.fillPoly(overlay, [np.array(pts)], (144, 238, 144))
            cv2.addWeighted(overlay, 0.4, output, 0.6, 0, output)

        y = 30
        for name in sorted(lane_counters):
            text = f"{name}: {lane_counters[name]}"
            cv2.putText(output, text, (10, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 4)
            cv2.putText(output, text, (10, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            y += 30

        out.write(output)
        frame_idx += 1

    cap.release()
    out.release()

    # Convert the temp .mp4 to H.264
    convert_to_h264(temp_output, output_path)
    os.remove(temp_output)