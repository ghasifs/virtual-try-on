import cv2
import numpy as np
from ultralytics import YOLO

# Load YOLO model
#model = YOLO("best.pt")  # Replace with the path to your trained model
model = YOLO("yolo11n-pose.pt")  # Replace with the path to your trained model

# Load the t-shirt image
t_shirt_image = cv2.imread("shirt_brown_tryon.png", cv2.IMREAD_UNCHANGED)

# Define key points on the t-shirt image (left/right shoulders and bottom left/right)
t_shirt_points = np.array([
    [93, 85],    # Left shoulder
    [265, 85],   # Right shoulder
    [135, 300],   # Bottom left
    [230, 300]   # Bottom right
], dtype="float32")

# Open the video
video_path = "sample.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Unable to open video.")
    exit()

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("End of video or error.")
        break

    # Perform YOLO inference
    results = model.predict(source=frame, imgsz=640, conf=0.3)

    # Check if detections exist
    if results[0].keypoints is not None and len(results[0].keypoints) > 0:
        keypoints = results[0].keypoints.xy[0].cpu().numpy()  # Shape: (17, 2)

        if len(keypoints) >= 13:  # Ensure indices 5, 6, 11, and 12 exist
            left_shoulder = keypoints[5]  # Index 5: Left Shoulder
            right_shoulder = keypoints[6]  # Index 6: Right Shoulder
            left_hip = keypoints[11]  # Index 11: Left Hip
            right_hip = keypoints[12]  # Index 12: Right Hip

            body_points = np.array([
                [left_shoulder[0], left_shoulder[1]],  # Left shoulder
                [right_shoulder[0], right_shoulder[1]],  # Right shoulder
                [left_hip[0], left_hip[1]],  # Left hip (Bottom left)
                [right_hip[0], right_hip[1]]  # Right hip (Bottom right)
            ], dtype="float32")

            H, _ = cv2.findHomography(t_shirt_points, body_points)
            warped_t_shirt = cv2.warpPerspective(t_shirt_image, H, (frame.shape[1], frame.shape[0]))

            # Overlay the t-shirt on the frame
            alpha = 0.7
            mask = (warped_t_shirt[:, :, 3] > 0).astype(np.uint8) * 255  # Use alpha channel as mask
            warped_rgb = warped_t_shirt[:, :, :3]
            frame_bg = cv2.bitwise_and(frame, frame, mask=cv2.bitwise_not(mask))
            t_shirt_fg = cv2.bitwise_and(warped_rgb, warped_rgb, mask=mask)
            frame = cv2.add(frame_bg, t_shirt_fg)
        else:
            print("Required keypoints not detected.")
    else:
        print("No detections in this frame.")
        
    cv2.imshow('T-Shirt Projection', frame)

    # Exit on pressing 'q'
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
