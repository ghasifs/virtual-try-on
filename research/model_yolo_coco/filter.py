import os
import json
from tqdm import tqdm

# Paths
COCO_TRAIN_JSON = "datasets/images/annotations/person_keypoints_train2017.json"
COCO_VAL_JSON = "datasets/images/annotations/person_keypoints_val2017.json"
TRAIN_IMAGES_DIR = "datasets/images/train2017"
VAL_IMAGES_DIR = "datasets/images/val2017"
LABELS_TRAIN_DIR = "datasets/labels/train"
LABELS_VAL_DIR = "datasets/labels/val"

# Create output directories
os.makedirs(LABELS_TRAIN_DIR, exist_ok=True)
os.makedirs(LABELS_VAL_DIR, exist_ok=True)

# Function to normalize coordinates
def normalize_bbox_and_keypoints(bbox, keypoints, img_width, img_height):
    x_center = (bbox[0] + bbox[2] / 2) / img_width
    y_center = (bbox[1] + bbox[3] / 2) / img_height
    width = bbox[2] / img_width
    height = bbox[3] / img_height

    normalized_keypoints = []
    for i in range(0, len(keypoints), 3):
        x, y, v = keypoints[i:i+3]
        if v > 0:  # Only normalize visible keypoints
            x /= img_width
            y /= img_height
        else:
            x, y = 0, 0  # If not visible, set to 0
        normalized_keypoints.extend([x, y, v])

    return x_center, y_center, width, height, normalized_keypoints

# Convert COCO annotations to YOLO format
def convert_coco_to_yolo(coco_json, images_dir, labels_dir):
    with open(coco_json, 'r') as f:
        coco_data = json.load(f)

    for annotation in tqdm(coco_data['annotations'], desc="Processing annotations"):
        image_id = annotation['image_id']
        image_info = next(img for img in coco_data['images'] if img['id'] == image_id)
        img_width, img_height = image_info['width'], image_info['height']
        img_name = image_info['file_name']

        # Extract bounding box and keypoints
        bbox = annotation['bbox']
        keypoints = annotation['keypoints']

        # Normalize data
        x_center, y_center, width, height, normalized_keypoints = normalize_bbox_and_keypoints(
            bbox, keypoints, img_width, img_height
        )

        # Create label file
        label_file = os.path.join(labels_dir, f"{os.path.splitext(img_name)[0]}.txt")
        with open(label_file, 'w') as f:
            f.write(f"0 {x_center} {y_center} {width} {height} " + " ".join(map(str, normalized_keypoints)) + "\n")

# Convert train and validation datasets
convert_coco_to_yolo(COCO_TRAIN_JSON, TRAIN_IMAGES_DIR, LABELS_TRAIN_DIR)
convert_coco_to_yolo(COCO_VAL_JSON, VAL_IMAGES_DIR, LABELS_VAL_DIR)
