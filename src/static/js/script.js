function previewImage() {
    const input = document.getElementById('imageInput');
    const file = input.files[0];
    const originalPreview = document.getElementById('originalPreview');

    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            originalPreview.src = e.target.result;
            originalPreview.style.display = 'block';
        }
        reader.readAsDataURL(file);
    } else {
        originalPreview.src = '#';
        originalPreview.style.display = 'none';
    }
}

async function uploadImage() {
    const input = document.getElementById('imageInput');
    const file = input.files[0];
    const resultBox = document.getElementById('result');
    const detectedCanvas = document.getElementById('detectedCanvas');
    detectedCanvas.style.display = 'none';

    if (!file) {
        alert('Please select an image first');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // 이미지 미리보기 src를 사용해서 캔버스에 그림
        const originalPreview = document.getElementById('originalPreview');
        const img = new window.Image();
        img.onload = function () {
            detectedCanvas.width = img.width;
            detectedCanvas.height = img.height;
            const ctx = detectedCanvas.getContext('2d');
            ctx.drawImage(img, 0, 0);

            // bbox 그리기
            if (data.detections && data.detections.length > 0) {
                ctx.strokeStyle = 'lime';
                ctx.lineWidth = 8; // 더 두껍게
                ctx.font = "bold 48px Arial"; // 글씨 더 크게
                ctx.textBaseline = "top";
                data.detections.forEach(det => {
                    if (det.bbox && det.bbox.length === 4) {
                        const [x1, y1, x2, y2] = det.bbox;
                        ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);

                        // 레이블 + confidence
                        const label = `${det.name} (${(det.confidence * 100).toFixed(1)}%)`;
                        // 배경 박스
                        const textWidth = ctx.measureText(label).width;
                        const textHeight = 32; // 높이도 더 크게
                        ctx.fillStyle = "rgba(0,0,0,0.7)";
                        ctx.fillRect(x1, y1 - textHeight, textWidth + 12, textHeight);
                        // 텍스트
                        ctx.fillStyle = "yellow";
                        ctx.fillText(label, x1 + 6, y1 - textHeight + 6);
                        ctx.fillStyle = "lime"; // 다시 원래 색상으로
                    }
                });
            }
            detectedCanvas.style.display = 'block';
        };
        img.src = originalPreview.src;

        // bbox 정보 텍스트 출력
        if (data.detections && data.detections.length > 0) {
            let text = `감지된 객체 수: ${data.detections.length}\n\n`;
            data.detections.forEach((det, idx) => {
                text += `[객체 ${idx + 1}]\n`;
                text += `- 클래스: ${det.name}\n`;
                text += `- 신뢰도: ${(det.confidence * 100).toFixed(2)}%\n`;
                if (det.bbox && det.bbox.length === 4) {
                    text += `- Bounding Box: [${det.bbox.map(v => v.toFixed(2)).join(', ')}]\n`;
                    text += `  * x1: ${det.bbox[0].toFixed(2)}\n`;
                    text += `  * y1: ${det.bbox[1].toFixed(2)}\n`;
                    text += `  * x2: ${det.bbox[2].toFixed(2)}\n`;
                    text += `  * y2: ${det.bbox[3].toFixed(2)}\n`;
                    text += `  * 너비: ${(det.bbox[2] - det.bbox[0]).toFixed(2)}\n`;
                    text += `  * 높이: ${(det.bbox[3] - det.bbox[1]).toFixed(2)}\n`;
                }
                text += '\n';
            });
            resultBox.textContent = text;
        } else {
            resultBox.textContent = '감지된 객체가 없습니다.';
        }
    } catch (error) {
        resultBox.textContent = '에러: ' + error.message;
    }
}