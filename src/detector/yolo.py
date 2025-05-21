from ultralytics import YOLO as UltralyticsYOLO
import numpy as np
import cv2
from typing import List, Dict

class YOLO:
    def __init__(self, model_path: str):
        self.model = UltralyticsYOLO(model_path)

    def detect(self, image_bytes: bytes) -> List[Dict]:
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        results = self.model(image)
        
        detections = []
        for r in results[0].boxes.data.tolist():
            x1, y1, x2, y2, conf, cls = r
            detection = {
                "bbox": [float(x1), float(y1), float(x2), float(y2)],
                "confidence": float(conf),
                "class": int(cls),
                "name": results[0].names[int(cls)]
            }
            detections.append(detection)
            
        return detections