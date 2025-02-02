import cv2

def generate_aruco_marker(marker_id, marker_size=200, output_path="aruco_marker.png"):
    # Initialize the ArUco dictionary
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_16h5)
    
    # Create the marker image
    marker = cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_size)
    
    # Save the marker image
    cv2.imwrite(output_path, marker)
    print(f"Marker ID {marker_id} saved to {output_path}")

# Generate markers with unique IDs
for marker_id in range(4):  # First four unique markers
    generate_aruco_marker(marker_id, output_path=f"marker_{marker_id}.png")
