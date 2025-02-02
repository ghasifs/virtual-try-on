
from ultralytics import YOLO

model = YOLO("best.pt")

results = model.predict(source="test.jpg", imgsz=640, save=True)

print(results[0].keypoints)