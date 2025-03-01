from roboflow import Roboflow
import cv2
import os

# Initialize Roboflow models
rf_1 = Roboflow(api_key="TiTpCb3EOE73TWRjXgrY")
project_1 = rf_1.workspace("hackathon25").project("vehicle-detection-and-management-9tjur-zyt7f")
model_1 = project_1.version(1).model

rf_2 = Roboflow(api_key="NflqMqokCB8LzO5ZnbjC")
project_2 = rf_2.workspace("hackathon2025-p8gqw").project("helmet-and-number-plate-detection-for-motorbike-safety-iityz-sfuvb")
model_2 = project_2.version(1).model

# Define function for processing video frames
def process_video_frame(frame):
    """Processes a single frame for vehicle detection and helmet violations."""
    cv2.imwrite("temp_frame.jpg", frame)  # Save frame as temporary image
    response = model_1.predict("temp_frame.jpg", confidence=40, overlap=30).json()

    vehicle_count = {'Car': 0, 'Bike': 0, 'Heavy Vehicle': 0}
    violations = []

    # Count detected vehicles
    for prediction in response['predictions']:
        class_name = prediction['class']
        if class_name in vehicle_count:
            vehicle_count[class_name] += 1

    print("Detected Vehicles:", vehicle_count)

    # Check for helmet violations
    helmet_detected = any(p['class'] == 'Helmet' for p in response['predictions'])
    
    for prediction in response['predictions']:
        if prediction['class'] == 'Bike' and not helmet_detected:
            print("Helmet Violation Detected!")
            violations.append(prediction.get('number_plate', 'Unknown'))  # Capture number plate if available

    return violations, vehicle_count

# Load video
video_path = r"C:\Users\mirdu\Downloads\Cars Moving On Road Stock Footage - Free Download.mp4"


# ✅ Ensure 'cap' is always initialized
cap = None  
if os.path.exists(video_path):
    cap = cv2.VideoCapture(video_path)

# ✅ Check if cap was successfully opened
if cap is not None and cap.isOpened():
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # Stop when the video ends
        
        # Process the frame
#        process_video_frame(frame)

    cap.release()  # Release only if cap was defined