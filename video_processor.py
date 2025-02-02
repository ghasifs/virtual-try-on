import cv2
import numpy as np
from ultralytics import YOLO
import mediapipe as mp

class ModelProcessor:
    """
    A class to process video frames using different models (Pose, YOLO, ArUco).
    Handles overlaying a virtual shirt on detected body landmarks.
    """
    def __init__(self, model_name, shirt_image_path, t_shirt_points):
        # Initialize the processor with the selected model and t-shirt details
        self.model_name = model_name.lower()
        self.shirt_image = cv2.imread(shirt_image_path, cv2.IMREAD_UNCHANGED)
        self.t_shirt_points = np.array(t_shirt_points, dtype="float32")
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=False, model_complexity=1)
        self.mp_drawing = mp.solutions.drawing_utils
        if model_name == "yolo":
            self.yolo_model = YOLO("static/models/yolo11n-pose.pt")
        elif model_name == "aruco":
            self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_16h5)
            self.aruco_params = cv2.aruco.DetectorParameters()

    def process_frame(self, frame):
        """
        Process a single frame using the selected model.
        """
        if self.model_name == "pose":
            return self._process_pose(frame)
        elif self.model_name == "yolo":
            return self._process_yolo(frame)
        elif self.model_name == "aruco":
            return self._process_aruco(frame)
        else:
            raise ValueError(f"Unsupported model: {self.model_name}")

    def _process_pose(self, frame):
        # Use MediaPipe Pose for detecting body landmarks
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(frame_rgb)

        if results.pose_landmarks:
            # Extract key body points for overlay
            landmarks = results.pose_landmarks.landmark
            body_points = np.array([
                [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER].x * frame.shape[1],
                 landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER].y * frame.shape[0]],
                [landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].x * frame.shape[1],
                 landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].y * frame.shape[0]],
                [landmarks[self.mp_pose.PoseLandmark.LEFT_HIP].x * frame.shape[1],
                 landmarks[self.mp_pose.PoseLandmark.LEFT_HIP].y * frame.shape[0]],
                [landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP].x * frame.shape[1],
                 landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP].y * frame.shape[0]]
            ], dtype="float32")

            return self._overlay_shirt(frame, body_points)
        return frame

    def _process_yolo(self, frame):
        # Use YOLO for detecting body keypoints
        results = self.yolo_model.predict(source=frame, imgsz=640, conf=0.3)
        if results[0].keypoints is not None:
            keypoints = results[0].keypoints.xy[0].cpu().numpy()
            if len(keypoints) >= 13:
                # Extract key body points for overlay
                body_points = np.array([
                    keypoints[5],  # Left shoulder
                    keypoints[6],  # Right shoulder
                    keypoints[11],  # Left hip
                    keypoints[12]   # Right hip
                ], dtype="float32")
                return self._overlay_shirt(frame, body_points)
        return frame

    def _process_aruco(self, frame):
        # Use ArUco markers for detecting predefined positions
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = cv2.aruco.detectMarkers(gray, self.aruco_dict, parameters=self.aruco_params)
        if ids is not None and len(ids) >= 4:
            marker_positions = {id: corner[0].mean(axis=0) for id, corner in zip(ids.flatten(), corners)}
            body_points = np.array([
                marker_positions[0],
                marker_positions[1],
                marker_positions[2],
                marker_positions[3]
            ], dtype="float32")
            return self._overlay_shirt(frame, body_points)
        return frame

    def _overlay_shirt(self, frame, body_points):
        """
        Overlay the t-shirt image on the frame using homography transformation.
        """
        H, _ = cv2.findHomography(self.t_shirt_points, body_points)
        warped_t_shirt = cv2.warpPerspective(self.shirt_image, H, (frame.shape[1], frame.shape[0]))
        mask = (warped_t_shirt[:, :, 3] > 0).astype(np.uint8) * 255
        warped_rgb = warped_t_shirt[:, :, :3]
        frame_bg = cv2.bitwise_and(frame, frame, mask=cv2.bitwise_not(mask))
        t_shirt_fg = cv2.bitwise_and(warped_rgb, warped_rgb, mask=mask)
        return cv2.add(frame_bg, t_shirt_fg)
