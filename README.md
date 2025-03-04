# ANPR Using YOLOv5  

## Description  
This project implements Automatic Number Plate Recognition (ANPR) using YOLOv5 for license plate detection and recognition. It provides two frontend interfaces:  
- **Flask-based Web Application**  
- **Streamlit-based Web Application**  

### Frontend-1 (Flask)  
![Flask UI](https://github.com/user-attachments/assets/b954c305-761f-44ce-a601-1efd51e133a8)  

### Frontend-2 (Streamlit)  
![Streamlit UI](https://github.com/user-attachments/assets/a675f52d-8375-430d-a9a3-9af37ced6291)  

---

## How to Run  
1. **Create a Conda Environment**  
   ```bash
   conda create -p yolo python=3.8 -y
   ```
2. **Clone YOLOv5 Repository**  
   ```bash
   git clone https://github.com/ultralytics/yolov5.git
   cd yolov5
   ```
3. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```
4. **Download Pretrained Weights**  
   - The model has been trained for **500 epochs** on labeled data.  
   - Download the `best.pt` weights file and place it in the `yolov5` directory.  

5. **Run the Application**  
   - **Flask App:**  
     ```bash
     python app.py
     ```
   - **Streamlit App:**  
     ```bash
     streamlit run app1.py
     ```

---

## Improvements and Potentials
- Train the model for **2000-3000 epochs** to improve real-time accuracy.  
- Optimize processing by **running the script on a GPU** for faster inference.
- For validation of output give by ocr , we use LLM model like Gemeni to remove unwanted ocr's.
- Instead of easy ocr we can use pysseract
