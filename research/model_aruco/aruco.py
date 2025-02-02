import cv2
import numpy as np

# Initialize the camera
cap = cv2.VideoCapture(1)

# Initialize the ArUco dictionary and detector
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_16h5)
aruco_params = cv2.aruco.DetectorParameters()

# Load the t-shirt image
t_shirt_image = cv2.imread("../images/shirt_brown_tryon.png", cv2.IMREAD_UNCHANGED)
if t_shirt_image is None:
    print("Error: T-shirt image not found.")

t_shirt_points = np.array([
    [93, 85],    # Left shoulder
    [265, 85],   # Right shoulder
    [135, 300],  # Bottom left
    [230, 300]   # Bottom right
], dtype="float32")

# Define the mapping of ArUco marker IDs to t-shirt points
marker_to_points = {
    0: "left_shoulder",
    1: "right_shoulder",
    2: "bottom_left",
    3: "bottom_right"
}

print("Starting the live ArUco detection... Press 'q' to quit.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame from camera.")
        break

    # Detect ArUco markers in the live feed
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)

    if ids is not None:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        marker_positions = {}
        for i, marker_id in enumerate(ids.flatten()):
            marker_positions[marker_id] = corners[i][0].mean(axis=0)

        if all(marker_id in marker_positions for marker_id in [0, 1, 2, 3]):
            body_points = np.array([
                marker_positions[0],  # Left shoulder
                marker_positions[1],  # Right shoulder
                marker_positions[2],  # Bottom left
                marker_positions[3]   # Bottom right
            ], dtype="float32")

            # Compute the homography and warp the t-shirt image
            H, _ = cv2.findHomography(t_shirt_points, body_points)
            warped_t_shirt = cv2.warpPerspective(t_shirt_image, H, (frame.shape[1], frame.shape[0]))

            # Overlay the t-shirt on the frame
            alpha = 0.7
            mask = (warped_t_shirt[:, :, 3] > 0).astype(np.uint8) * 255  # Alpha channel as mask
            warped_rgb = warped_t_shirt[:, :, :3]
            frame_bg = cv2.bitwise_and(frame, frame, mask=cv2.bitwise_not(mask))
            t_shirt_fg = cv2.bitwise_and(warped_rgb, warped_rgb, mask=mask)
            frame = cv2.add(frame_bg, t_shirt_fg)

    cv2.imshow("Live Virtual Try-On", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
