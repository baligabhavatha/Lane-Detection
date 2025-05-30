import streamlit as st
import tempfile
import os
from pathlib import Path
from process_video import run_yolo_processing  # Your function in a separate file

st.set_page_config(page_title="Vehicle Lane Counter", layout="centered")
st.title("🚦 Lane-wise Vehicle Counting")

# Session state to prevent re-processing
if "video_processed" not in st.session_state:
    st.session_state.video_processed = False
if "input_path" not in st.session_state:
    st.session_state.input_path = None
if "output_path" not in st.session_state:
    st.session_state.output_path = "output_processed.mp4"

uploaded_file = st.file_uploader("📤 Upload a video file", type=["mp4"])

# Save uploaded file only once
if uploaded_file is not None and not st.session_state.input_path:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(uploaded_file.read())
        st.session_state.input_path = tmp.name
    st.success("✅ File uploaded. Now click 'Process Video'.")

# Manual trigger for processing
if st.button("⚙️ Process Video") and st.session_state.input_path:
    with st.spinner("⏳ Please hold on, processing your video..."):
        run_yolo_processing(st.session_state.input_path, st.session_state.output_path, duration_sec=15)
    st.session_state.video_processed = True
    st.success("✅ Video processed successfully!")

# Show and allow download only if processed
if st.session_state.video_processed:
    st.success("✅ Video processed successfully!")
    try:
        st.video(st.session_state.output_path, format="video/mp4")  # Preview
    except Exception as e:
        st.warning(f"Unable to preview video: {e}")
    with open(st.session_state.output_path, "rb") as f:
        st.download_button("⬇️ Download Processed Video", f, file_name="processed.mp4")



    # with open(output_path, "rb") as file:
    #     st.download_button("📥 Download Processed Video", file, file_name="processed_video.mp4")
