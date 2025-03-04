# import os
# import easyocr
# # from langchain_google_genai import ChatGoogleGenerativeAI
# # from langchain_core.promp
# def extract_unique_license_plates(folder_path):
#     reader = easyocr.Reader(['en'])
#     license_plates = set()
#     # Loop through the cropped images
#     for filename in os.listdir(folder_path):
#         if filename.endswith(('.png', '.jpg', '.jpeg')):
#             image_path = os.path.join(folder_path, filename)
            
#             # Use EasyOCR to read the license plate text
#             result = reader.readtext(image_path, detail=0)
            
#             for _,text,confi in result:
#                 # Clean the text a bit (remove spaces, convert to uppercase)
#                 if(confi>0.5):
#                     # plate = text.replace(" ", "").upper()
#                     plate = text.upper()
#                     license_plates.add(plate)
#                     # Plot the image 

#     return license_plates
import os
import easyocr

def extract_unique_license_plates(folder_path):
    reader = easyocr.Reader(['en'])
    license_plates = {}
    # Loop through the cropped images
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            
            # Use EasyOCR to read the license plate text
            result = reader.readtext(image_path, detail=0)
            
            for _,text,confi in result:
                # Clean the text a bit (remove spaces, convert to uppercase)
                if(confi>0.5):
                    # plate = text.replace(" ", "").upper()
                    plate = text.upper()
                    # Plot the image 
                    # Store only if plate is NOT already in the dictionary
                    if plate not in license_plates:
                        license_plates[plate] = {
                            "image_path": image_path,
                            "confidence": round(confi, 2)
                        }

    return license_plates