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
   run_server.bat
   ```
   여기에는 다음과 같은 코드가 들어 있다.
   ```
   REM filepath: d:\DEV_23\restAPI2\run_server.bat
   @echo off
   set PYTHONPATH=%cd%\src
   uvicorn main:app --reload --host 0.0.0.0 --port 8080
   ```
2. 실행화면 
## 테스트 화면   웹 브라우저에서    
   ```
   http://localhost:8080/static/index.html
   ```
   로 접속 하면    
   ![image](https://github.com/user-attachments/assets/9a767fc1-a1ef-495b-a762-a4db19a88d36)

3. API 사용 설명서는 `http://127.0.0.1:8080/docs`.

4. curl과 python code test
   ```
   cd tests
   cmd_test.bat
   ```
   내부에는  다음과 같은 코드가 들어 있다.
   ```
   echo off
   echo.
   echo ====================== curl test 결과 출력 ======================
   curl -X POST -F "file=@너의 이미지 파일" http://localhost:8080/upload
   echo.
   echo ====================== curl test finish   ======================
   echo.
   echo.
   echo ====================== test_api.py 실행   ======================
   echo.
   pytest test_api.py -vv --capture=no
   echo.
   echo ====================== test_api.py finish ======================
   ```

## 테스트 화면 콘솔에서 
![image](https://github.com/user-attachments/assets/3e64c4cc-f2b2-4d9c-8994-0f292a106347)
![image](https://github.com/user-attachments/assets/3b4612e1-04e5-4c60-836c-d77b2cddce8e)


   

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
