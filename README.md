# README.md

# Object Detection API

This project is a FastAPI application that allows users to upload images and perform object detection using the YOLOv8 model. The API processes the uploaded images and returns the detected objects along with their confidence scores.

## Features

- Upload images for object detection
- Detect objects in images using YOLOv8
- Return structured JSON responses with detection results

## Project Structure

```
object-detection-api
├── src
│   ├── main.py          # Entry point of the application
│   ├── detector         # Module for object detection
│   │   ├── __init__.py
│   │   └── yolo.py      # YOLO class for detection
│   ├── models           # Module for data models
│   │   └── __init__.py
│   ├── schemas          # Module for response schemas
│   │   └── response.py   # Defines response structure
│   ├── utils            # Module for utility functions
│   │   ├── __init__.py
│   │   └── image.py     # Image processing utilities
│   └── config.py       # Configuration settings
├── tests                # Directory for unit tests
│   └── test_api.py      # Tests for API endpoints
├── .env                 # Environment variables
├── .gitignore           # Git ignore file
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd object-detection-api
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the FastAPI server:
   ```
   uvicorn src.main:app --reload
   ```

2. Access the API documentation at `http://127.0.0.1:8000/docs`.

3. Use the `/upload` endpoint to upload images for object detection.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.