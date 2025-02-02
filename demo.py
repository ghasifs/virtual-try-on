import cv2
from video_processor import ModelProcessor
from config import SHIRT_IMAGES, T_SHIRT_POINTS

# Initialize the ModelProcessor with Mediapipe pose detection
processor = ModelProcessor(
    model_name="yolo",  # Change to "yolo" or "aruco" for other detection methods
    shirt_image_path=SHIRT_IMAGES["shirt_brown"], # Change to other shirt colors
    t_shirt_points=T_SHIRT_POINTS
)

# Load demo images
demo_images = [
    "static/images/test_model.jpg",
    "static/images/test_model2.jpg"
]

# Process each demo image
for idx, image_path in enumerate(demo_images):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to load image {image_path}")
        continue

    # Run inference and overlay the shirt
    result = processor.process_frame(image)

    # Resize to fit the screen
    result = cv2.resize(result, (1280, 720))
    
    cv2.imshow(f"Result {idx + 1}", result)
    cv2.waitKey(0)

cv2.destroyAllWindows()
