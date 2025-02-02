import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, model_complexity=1, enable_segmentation=False, min_detection_confidence=0.5)

# Initialize drawing utilities
mp_drawing = mp.solutions.drawing_utils

# Load the video and t-shirt image
video_path = "videos/sample.mp4"
t_shirt_image = cv2.imread("images/shirt_brown_tryon.png", cv2.IMREAD_UNCHANGED)

# Define key points on the t-shirt image
t_shirt_points = np.array([
    [93, 85],    # Left shoulder
    [265, 85],   # Right shoulder
    [135, 300],   # Bottom left
    [230, 300]   # Bottom right
], dtype="float32")

cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("End of video or error.")
        break

    # Convert frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    # If pose landmarks are detected
    if results.pose_landmarks:
        # Retrieve the shoulder and hip landmarks
        left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]

        # Create corresponding body points array for homography
        body_points = np.array([
            [left_shoulder.x * frame.shape[1], left_shoulder.y * frame.shape[0]],  # Left shoulder
            [right_shoulder.x * frame.shape[1], right_shoulder.y * frame.shape[0]],  # Right shoulder
            [left_hip.x * frame.shape[1], left_hip.y * frame.shape[0]],  # Left hip (Bottom left)
            [right_hip.x * frame.shape[1], right_hip.y * frame.shape[0]]  # Right hip (Bottom right)
        ], dtype="float32")

        # Compute homography matrix
        H, _ = cv2.findHomography(t_shirt_points, body_points)

        # Warp the t-shirt image to fit the body
        warped_t_shirt = cv2.warpPerspective(t_shirt_image, H, (frame.shape[1], frame.shape[0]))

        # Overlay the t-shirt onto the frame with transparency
        alpha = 0.7
        mask = (warped_t_shirt[:, :, 3] > 0).astype(np.uint8) * 255  # Use alpha channel as mask
        warped_rgb = warped_t_shirt[:, :, :3]
        frame_bg = cv2.bitwise_and(frame, frame, mask=cv2.bitwise_not(mask))
        t_shirt_fg = cv2.bitwise_and(warped_rgb, warped_rgb, mask=mask)
        frame = cv2.add(frame_bg, t_shirt_fg)

        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Display the frame
    cv2.imshow('T-Shirt Projection', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
