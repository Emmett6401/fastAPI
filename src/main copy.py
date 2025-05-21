from fastapi import FastAPI, HTTPException, File, UploadFile, Request
from fastapi.responses import JSONResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from detector.yolo import YOLO  # YOLO 모델 import (절대 경로)
from schemas.response import DetectionResponse
import os
import logging
from pathlib import Path
import time
from io import BytesIO
import cv2  # OpenCV import
import numpy as np  # NumPy import

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(debug=True)  # debug 모드 활성화

# Static files configuration
current_dir = Path(__file__).parent.absolute()  # 현재 파일의 절대 경로
project_root = current_dir.parent  # 프로젝트 루트 경로
static_dir = current_dir / "static"  # static 파일 경로

# Mount static files (정적 파일 제공 설정)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# index.html 파일 제공 (HTML 응답)
@app.get("/index")
async def get_index():
    file_path = os.path.join(os.path.dirname(__file__), "static", "index.html")  # index.html 파일 경로
    if os.path.exists(file_path):  # 파일 존재 확인
        with open(file_path, "r", encoding="utf-8") as f:  # 파일 읽기 (UTF-8 인코딩)
            html_content = f.read()  # HTML 내용 읽기
        return HTMLResponse(content=html_content)  # HTML 응답 반환
    else:
        return {"error": "File not found"}  # 파일이 없을 경우 에러 반환

# 루트 경로 (/) 접속 시 HTML 응답 반환
@app.get("/")
async def read_root():
    return HTMLResponse(content="""
    <html>
        <head>
            <title>YOLO Detection Test</title>
        </head>
        <body>
            <h1>YOLO Detection Test</h1>
                        
            <a href="/static/index.html">Go to index.html</a>
        </body>
    </html>
    """)

# 디버깅 경로 정보 제공 (JSON 응답)
@app.get("/debug/paths")
async def debug_paths():
    return {
        "current_dir": str(current_dir),  # 현재 디렉토리 경로
        "project_root": str(project_root),  # 프로젝트 루트 경로
        "static_dir": str(static_dir),  # static 파일 경로
        "static_files": os.listdir(static_dir) if os.path.exists(static_dir) else []  # static 파일 목록
    }

# YOLO 모델 초기화
try:
    model_path = os.getenv("YOLO_MODEL_PATH", "yolov8n.pt")  # 환경 변수에서 모델 경로 가져오기
    # data_path = os.getenv("YOLO_DATA_PATH", "data.yaml")  # 환경 변수에서 데이터 경로 가져오기
    app.state.yolo_model = YOLO(model_path=model_path)  # YOLO 모델 초기화
    logger.info(f"YOLO model loaded successfully from {model_path}")  # 로그 메시지
except Exception as e:
    logger.error(f"Error initializing YOLO model: {str(e)}")  # 에러 로그 메시지
    raise  # 예외 다시 발생

# 이미지 업로드 및 객체 탐지 (POST 요청)
@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    # Check file type (파일 타입 확인)
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only images are allowed."  # 에러 메시지
        )

    try:
        contents = await file.read()  # 파일 내용 읽기
        img_stream = BytesIO(contents)  # BytesIO 객체 생성
        img_array = np.asarray(bytearray(img_stream.read()), dtype=np.uint8)  # NumPy 배열로 변환
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # OpenCV를 사용하여 이미지 디코딩

        if img is None:
            raise HTTPException(status_code=400, detail="Could not decode image")

        detections = app.state.yolo_model.detect(img)  # YOLO 모델로 객체 탐지

        # Bounding box 그리기
        for detection in detections:  # 탐지된 객체 정보 순회
            try:
                boxes = detection.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]  # bounding box 좌표 추출
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 이미지에 bounding box 그리기 (초록색)
            except ValueError as e:
                logger.error(f"Error processing bounding box: {str(e)}")
                continue

        img_bytes = cv2.imencode('.jpg', img)[1].tobytes()  # 이미지 인코딩 (.jpg 형식)

        # StreamingResponse로 이미지 반환 (media_type: image/jpeg)
        return StreamingResponse(BytesIO(img_bytes), media_type="image/jpeg")

    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")  # 에러 로그 메시지
        raise HTTPException(status_code=500, detail=str(e))  # 예외 다시 발생

# 404 에러 핸들러 (Not Found)
@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    logger.error(f"Route not found: {request.url}")  # 에러 로그 메시지
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Not Found",  # 에러 상세 정보
            "requested_path": str(request.url),  # 요청 경로
            "available_static_files": os.listdir(static_dir) if os.path.exists(static_dir) else []  # 사용 가능한 static 파일 목록
        }
    )

# 테스트 엔드포인트 (/test)
@app.get("/test")
async def test():
    return {"message": "Hello, World!"}  # JSON 응답 반환

# 서버 종료 함수
async def shutdown(loop):
    print("Shutting down...")
    loop.stop()  # 이벤트 루프 중단

# 메인 함수 (asyncio)
async def main():
    loop = asyncio.get_event_loop()  # 이벤트 루프 가져오기
    loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(shutdown(loop)))  # SIGINT 신호 처리

# 메인 스크립트 실행
if __name__ == "__main__":
    asyncio.run(main())  # asyncio 런타임으로 메인 함수 실행