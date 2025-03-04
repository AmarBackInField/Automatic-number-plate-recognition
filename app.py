import os
import cv2
import torch
import easyocr
import pandas as pd
import numpy as np
from pathlib import Path
import pathlib
from flask import Flask, render_template, request, send_file, jsonify
import werkzeug

# Ensure Windows path compatibility 
pathlib.PosixPath = pathlib.WindowsPath

# Initialize Flask app
app = Flask(__name__)
BASE_DIR=os.getcwd()
# Configure upload and output folders
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load YOLOv5 model
MODEL_PATH = "best.pt"  # Replace with your trained model path
model = torch.hub.load("ultralytics/yolov5", "custom", path=MODEL_PATH, force_reload=True)

def extract_unique_license_plates(folder_path):
    """
    Extract unique license plate texts along with their image paths.
    Returns: Dictionary {plate_text: image_path}
    """
    reader = easyocr.Reader(['en'])
    license_plates = {}

    try:
        for filename in os.listdir(folder_path):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(folder_path, filename)
                results = reader.readtext(image_path)
                
                for _, text, confi in results:
                    if confi > 0.6:
                        plate = text.upper()
                        license_plates[plate] = image_path
    except Exception as e:
        print(f"Error extracting license plates: {e}")
    
    return license_plates

@app.route('/', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'video' not in request.files:
            return render_template('index.html', error='No file uploaded')
        
        video = request.files['video']
        
        # Check if filename is empty
        if video.filename == '':
            return render_template('index.html', error='No selected file')
        
        # Save the uploaded video
        if video:
            # Secure the filename
            filename = werkzeug.utils.secure_filename(video.filename)
            video_path = os.path.join(UPLOAD_FOLDER, filename)
            video.save(video_path)
            
            # Prepare output folders
            # output_folder = os.path.join(OUTPUT_FOLDER, "detected", "crops", "License-Plate")
            # output_folder = "outputed/detected/crops/License-Plate"
            # os.makedirs("outputed", exist_ok=True)
            output_folder = os.path.join(OUTPUT_FOLDER, "detected", "crops", "License-Plate")
            os.makedirs(output_folder, exist_ok=True)

            # os.makedirs(output_folder, exist_ok=True)
            print(output_folder)
            
            os.system(f"python yolov5/detect.py --weights {MODEL_PATH} --source {video_path} --conf 0.5 --save-txt --save-crop --project outputed --name detected")

            
            # Extract license plates
            plate_dict = extract_unique_license_plates(output_folder)
            print(plate_dict)
            # Prepare data for CSV and display
            data = []
            for plate, img_path in plate_dict.items():
                data.append({"Plate Number": plate, "Image Path": img_path})
            
            # Create DataFrame and save to CSV
            df = pd.DataFrame(data)
            csv_path = os.path.join(OUTPUT_FOLDER, "detected_plates.csv")
            df.to_csv(csv_path, index=False)
            
            # Determine output video path
            # output_video_path = os.path.join(
            #     output_folder, 
            #     f"{Path(video_path).stem}.mp4"
            # )
            output_video_path = os.path.join(
                BASE_DIR,OUTPUT_FOLDER, "detected", f"{Path(video_path).stem}.mp4"
            )

            print(output_video_path)
            return render_template(
                'results.html', 
                plates=plate_dict, 
                csv_path=csv_path,
                video_path=output_video_path
            )
    
    return render_template('index.html')

@app.route('/download_csv')
def download_csv():
    """Route to download the CSV file"""
    csv_path = os.path.join(OUTPUT_FOLDER, "detected_plates.csv")
    return send_file(csv_path, as_attachment=True)

@app.route('/download_plate_image/<path:image_path>')
def download_plate_image(image_path):
    """Route to download a specific plate image"""
    return send_file(image_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)