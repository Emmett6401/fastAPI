import os
import sys
from pathlib import Path

# Add project root and src directory to Python path
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.extend([str(project_root), str(src_path)])

import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_upload_image():
    # 테스트 이미지 경로
    test_image = "D:/Pictures/KakaoTalk_20230505_164421070_08.jpg"

    with open(test_image, "rb") as image_file:
        files = {"file": ("test_image.jpg", image_file, "image/jpeg")}
        response = client.post("/upload", files=files)

    # 결과 출력 정리
    print("\n" + "="*50)
    print("테스트 결과 요약")
    print("="*50)
    print(f"상태 코드: {response.status_code}")
    print("-"*50)   
    
    if response.headers.get("content-type", "").startswith("application/json"):
        try:
            result = response.json()    
            # 감지된 객체 정보 출력 
            if "detections" in result:
                print(f"감지된 객체 수: {len(result.get('detections', []))}")
                print("-"*50)
                print("감지된 객체 세부 정보:")
                print("-"*50)
                for idx, detection in enumerate(result["detections"], 1):
                    print(f"\n[객체 {idx}]")
                    print(f"- 클래스 ID: {detection.get('class', 'N/A')}")
                    print(f"- 클래스 이름: {detection.get('name', 'N/A')}")
                    print(f"- 신뢰도: {detection.get('confidence', 0):.2%}")
                    
                    # bbox 정보 출력
                    bbox = detection.get('bbox', [])
                    if len(bbox) == 4:  # [x1, y1, x2, y2] 형식
                        print(f"- Bounding Box:")
                        print(f"  * x1: {bbox[0]:.2f}")
                        print(f"  * y1: {bbox[1]:.2f}")
                        print(f"  * x2: {bbox[2]:.2f}")
                        print(f"  * y2: {bbox[3]:.2f}")
                        print(f"  * 너비: {bbox[2] - bbox[0]:.2f}")
                        print(f"  * 높이: {bbox[3] - bbox[1]:.2f}")

        except Exception as e:
            print("예외 발생:", repr(e))
            with open("result.jpg", "wb") as f:
                f.write(response.content)
            print("리턴 값이 이미지 파일이므로 result.jpg로 이미지 저장 완료")
    else:
        print("JSON이 아닌 응답입니다. content-type:", response.headers.get("content-type"))