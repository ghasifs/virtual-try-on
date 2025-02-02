# import cv2
# import numpy as np

# # Map ArUco marker IDs to t-shirt key points
# marker_to_points = {
#     0: "left_shoulder",
#     1: "right_shoulder",
#     2: "bottom_left",
#     3: "bottom_right"
# }

# # Load the test image with ArUco markers
# test_image_path = "../images/test_with_markers.png"
# test_image = cv2.imread(test_image_path)

# # Initialize the ArUco dictionary and detector
# aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_16h5)
# aruco_params = cv2.aruco.DetectorParameters()

# # Detect ArUco markers in the test image
# corners, ids, _ = cv2.aruco.detectMarkers(test_image, aruco_dict, parameters=aruco_params)

# if ids is not None:
#     print("Detected marker positions:")
#     marker_positions = {}
    
#     # Map each detected marker to its corresponding t-shirt point
#     for i, marker_id in enumerate(ids.flatten()):
#         marker_position = corners[i][0]  # Marker corners
#         marker_positions[marker_id] = marker_position.mean(axis=0)  # Get center of marker
#         t_shirt_point = marker_to_points.get(marker_id, "unknown")
#         print(f"Marker ID {marker_id} ({t_shirt_point}): {marker_positions[marker_id]}")

#     # Draw markers for visualization
#     cv2.aruco.drawDetectedMarkers(test_image, corners, ids)
#     cv2.imshow("Detected Markers", test_image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
# else:
#     print("No markers detected!")

####################################

import cv2
import numpy as np

# Load the t-shirt image and test image
t_shirt_image = cv2.imread("../images/shirt_brown_tryon.png", cv2.IMREAD_UNCHANGED)
test_image = cv2.imread("../images/test_with_markers.png")

# Detect ArUco markers
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_16h5)
aruco_params = cv2.aruco.DetectorParameters()
corners, ids, _ = cv2.aruco.detectMarkers(test_image, aruco_dict, parameters=aruco_params)

if ids is not None:
    # Map detected markers to body points
    marker_positions = {}
    for i, marker_id in enumerate(ids.flatten()):
        marker_positions[marker_id] = corners[i][0].mean(axis=0)

    # Define the body points based on marker IDs
    body_points = np.array([
        marker_positions[0],  # Left shoulder
        marker_positions[1],  # Right shoulder
        marker_positions[2],  # Bottom left
        marker_positions[3]   # Bottom right
    ], dtype="float32")

    # Define corresponding points on the t-shirt image
    t_shirt_points = np.array([
        [93, 85],    # Left shoulder
        [265, 85],   # Right shoulder
        [135, 300],  # Bottom left
        [230, 300]   # Bottom right
    ], dtype="float32")

    # Compute homography and warp the t-shirt
    H, _ = cv2.findHomography(t_shirt_points, body_points)
    warped_t_shirt = cv2.warpPerspective(t_shirt_image, H, (test_image.shape[1], test_image.shape[0]))

    # Overlay the t-shirt on the test image
    alpha = 0.7
    mask = (warped_t_shirt[:, :, 3] > 0).astype(np.uint8) * 255
    warped_rgb = warped_t_shirt[:, :, :3]
    test_image_bg = cv2.bitwise_and(test_image, test_image, mask=cv2.bitwise_not(mask))
    t_shirt_fg = cv2.bitwise_and(warped_rgb, warped_rgb, mask=mask)
    result = cv2.add(test_image_bg, t_shirt_fg)

    # Display the result
    cv2.imshow("Virtual Try-On", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No markers detected!")
