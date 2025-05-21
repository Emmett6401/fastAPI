import os

class Config:
    # Path to the YOLOv8 model
    MODEL_PATH = os.getenv("MODEL_PATH", "path/to/yolov8/model")
    
    # Allowed image extensions
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Maximum file size for uploads (in bytes)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

    # API settings
    API_TITLE = "Object Detection API"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = "API for uploading images and detecting objects using YOLOv8."