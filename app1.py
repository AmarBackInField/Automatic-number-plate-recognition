import streamlit as st
import os
import cv2
import torch
import easyocr
import pandas as pd
import numpy as np
from pathlib import Path
import pathlib
import time

pathlib.PosixPath = pathlib.WindowsPath

# Load YOLOv5 model
model_path = "best.pt"  # Replace with your trained model
model = torch.hub.load("ultralytics/yolov5", "custom", path=model_path, force_reload=True)

def extract_unique_license_plates(folder_path):
    """
    Extract unique license plate texts along with their image paths.
    Returns: Dictionary {plate_text: image_path}
    """
    reader = easyocr.Reader(['en'])
    license_plates = {}

    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            results = reader.readtext(image_path)
            
            for _, text, confi in results:
                if confi > 0.5:
                    plate = text.upper()
                    license_plates[plate] = image_path

    return license_plates

# Streamlit UI
st.title("🔍 License Plate Detection")
st.write("Upload a video to detect license plates.")

uploaded_file = st.file_uploader("Choose a video...", type=["mp4", "webm", "avi", "mov"])

if uploaded_file is not None:
    os.makedirs("uploads", exist_ok=True)
    video_path = f"uploads/{uploaded_file.name}"
    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())
    
    st.success(f"✅ Video uploaded successfully: {uploaded_file.name}")

    # Progress bar
    progress_bar = st.progress(0)
    st.write("⏳ Processing video with YOLOv5...")
    
    output_folder = "outputss/detected/crops/License-Plate"
    os.makedirs("outputs", exist_ok=True)
    
    os.system(f"python yolov5/detect.py --weights {model_path} --source {video_path} --conf 0.5 --save-txt --save-crop --project outputss --name detected")
    
    progress_bar.progress(50)
    st.write("🔎 Extracting license plates...")
    
    plate_dict = extract_unique_license_plates(output_folder)
    progress_bar.progress(80)
    
    # Show results
    st.subheader("📸 Detected License Plates:")
    
    if plate_dict:
        data = []
        for plate, img_path in plate_dict.items():
            col1, col2 = st.columns([1, 4])
            with col1:
                st.image(img_path, caption=f"Plate: {plate}", width=200)
            with col2:
                st.subheader(plate)
            data.append({"Plate Number": plate, "Image Path": img_path})

        # Save results as CSV
        df = pd.DataFrame(data)
        csv_path = "outputs/detected_plates.csv"
        df.to_csv(csv_path, index=False)
        
        # Download CSV button
        st.download_button(
            label="📥 Download License Plate Data as CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name="detected_plates.csv",
            mime='text/csv',
        )
    else:
        st.warning("⚠️ No license plates detected. Try uploading a clearer video.")

    progress_bar.progress(100)
    
    # Show processed video
    output_video_path = f"outputs/{Path(video_path).stem}_output.mp4"
    st.subheader("🎥 Processed Video:")
    st.video(output_video_path)

else:
    st.info("Upload a video to get started!")
