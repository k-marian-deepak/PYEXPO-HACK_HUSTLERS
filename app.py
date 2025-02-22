import cv2
from roboflow_dataset import process_video_frame
from main_traffic_logic import process_traffic_data

# Open the video file
video_path = "Cars Moving On Road Stock Footage - Free Download.mp4"
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Process the frame
    vehicle_count, violations = process_video_frame(frame)

    # Update traffic logic based on vehicle counts
    traffic_signals = process_traffic_data(vehicle_count)

    # Display the frame (optional)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
