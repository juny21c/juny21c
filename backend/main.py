"""
얼굴 관상 분석 서비스 백엔드 API
FastAPI를 사용하여 얼굴 사진 업로드 및 관상 분석 기능 제공
"""

import os
import uuid
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# API 제공자 선택 (환경 변수에서 읽기, 기본값: gemini)
API_PROVIDER = os.getenv("API_PROVIDER", "gemini").lower()

# 선택한 API에 따라 적절한 FaceReader 임포트
if API_PROVIDER == "gemini":
    from face_reader_gemini import FaceReaderGemini as FaceReader
    print("🌟 Google Gemini API를 사용합니다")
else:
    from face_reader import FaceReader
    print("🔮 Anthropic Claude API를 사용합니다")

# FastAPI 앱 생성
app = FastAPI(
    title="얼굴 관상 분석 서비스",
    description="AI를 활용한 얼굴 관상 분석 API",
    version="1.0.0"
)

# CORS 설정 (프론트엔드와 통신 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 업로드 디렉토리 설정
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# FaceReader 인스턴스 생성
face_reader = FaceReader()


@app.get("/")
async def root():
    """API 상태 확인"""
    return {
        "message": "얼굴 관상 분석 API",
        "status": "running",
        "version": "1.0.0",
        "api_provider": API_PROVIDER
    }


@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"}


@app.post("/api/analyze")
async def analyze_face(file: UploadFile = File(...)):
    """
    얼굴 사진을 업로드하고 관상 분석 결과를 반환

    Args:
        file: 업로드된 이미지 파일

    Returns:
        관상 분석 결과
    """
    # 파일 형식 검증
    allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
    file_extension = file.filename.split('.')[-1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"지원하지 않는 파일 형식입니다. 허용된 형식: {', '.join(allowed_extensions)}"
        )

    try:
        # 고유한 파일명 생성
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = UPLOAD_DIR / unique_filename

        # 파일 저장
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        # 관상 분석 수행
        result = face_reader.analyze_face(str(file_path))

        # 임시 파일 삭제
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"임시 파일 삭제 실패: {e}")

        # 결과 반환
        if result["success"]:
            return JSONResponse(content={
                "success": True,
                "analysis": result["analysis"],
                "model": result.get("model", "unknown")
            })
        else:
            raise HTTPException(
                status_code=500,
                detail=f"관상 분석 실패: {result.get('error', '알 수 없는 오류')}"
            )

    except HTTPException:
        raise
    except Exception as e:
        # 에러 발생 시 임시 파일 정리
        if 'file_path' in locals() and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass

        raise HTTPException(
            status_code=500,
            detail=f"서버 오류: {str(e)}"
        )


@app.delete("/api/cleanup")
async def cleanup_uploads():
    """업로드 디렉토리의 임시 파일들을 정리"""
    try:
        count = 0
        for file_path in UPLOAD_DIR.glob("*"):
            if file_path.is_file():
                os.remove(file_path)
                count += 1
        return {"message": f"{count}개의 임시 파일이 삭제되었습니다."}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"정리 실패: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
