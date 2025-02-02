# Path to the YOLO model used for pose detection
YOLO_MODEL_PATH = "static/models/yolo11n-pose.pt"

# Path to the test video used in the application ('0' for webcam)
VIDEO_PATH = "static/videos/test_video.mp4"

# Mapping of shirt IDs to their corresponding overlay images
SHIRT_IMAGES = {
    'shirt_natural': "static/images/shirt_natural_tryon.png",
    'shirt_blue': "static/images/shirt_blue_tryon.png",
    'shirt_brown': "static/images/shirt_brown_tryon.png",
    'shirt_black': "static/images/shirt_black_tryon.png",
}

# Predefined points on the t-shirt image for perspective mapping
T_SHIRT_POINTS = [
    [93, 85],    # Left shoulder
    [265, 85],   # Right shoulder
    [135, 300],  # Bottom left
    [230, 300],  # Bottom right
]
