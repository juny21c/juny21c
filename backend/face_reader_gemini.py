"""
얼굴 관상 분석 모듈 - Google Gemini 버전
Google Gemini Vision API를 사용하여 얼굴 사진을 분석하고 관상을 해석합니다.
"""

import os
from typing import Dict, Any
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class FaceReaderGemini:
    """얼굴 관상 분석 클래스 - Gemini 버전"""

    def __init__(self):
        """API 키로 Gemini 클라이언트 초기화"""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY 환경 변수가 설정되지 않았습니다.")

        genai.configure(api_key=api_key)

        # 사용 가능한 모델 목록 출력 (디버깅용)
        try:
            available_models = [m.name for m in genai.list_models()]
            print(f"📋 사용 가능한 Gemini 모델: {available_models}")
        except Exception as e:
            print(f"⚠️ 모델 목록 조회 실패: {e}")

        # 지원되는 모델 시도 (우선순위대로) - 2025년 최신 모델
        model_candidates = [
            'models/gemini-2.5-flash',
            'models/gemini-2.0-flash',
            'models/gemini-flash-latest',
            'models/gemini-2.5-pro',
            'models/gemini-pro-latest',
        ]

        model_name = None
        for candidate in model_candidates:
            try:
                self.model = genai.GenerativeModel(candidate)
                model_name = candidate
                print(f"✅ 모델 선택 성공: {candidate}")
                break
            except Exception as e:
                print(f"❌ 모델 {candidate} 실패: {e}")
                continue

        if not model_name:
            raise ValueError("사용 가능한 Gemini 모델을 찾을 수 없습니다.")

    def analyze_face(self, image_path: str) -> Dict[str, Any]:
        """
        얼굴 사진을 분석하여 관상을 해석

        Args:
            image_path: 분석할 얼굴 사진 경로

        Returns:
            관상 분석 결과 딕셔너리
        """
        try:
            # 이미지 로드
            image = Image.open(image_path)

            # 프롬프트 생성 (60대 여성 타겟 맞춤)
            prompt = """이 얼굴 사진을 보고 관상을 분석해주세요. 60대 여성분이 보시는 내용이니 따뜻하고 희망적으로 작성해주세요.

**건강운과 장수**
건강 상태와 앞으로의 건강 관리 조언 (3줄)

**자녀운과 가족복**
자녀, 손주와의 관계, 가족의 발전 (3줄)

**금전운과 재물**
노후 경제 상황, 재물 관리, 뜻밖의 행운 (3줄)

**인복과 친구운**
주변 사람들과의 관계, 새로운 인연 (3줄)

**말년 운세와 행복**
앞으로의 삶, 취미, 여유로운 노후, 격려의 말 (4줄)

60대 여성분들이 듣고 싶어하는 따뜻하고 긍정적인 내용으로 작성해주세요. 구체적이고 실질적인 조언을 포함하되, 희망과 위로를 담아주세요."""

            # Gemini API 호출 (safety settings 추가)
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE"
                },
            ]

            response = self.model.generate_content(
                [prompt, image],
                safety_settings=safety_settings
            )

            return {
                "success": True,
                "analysis": response.text,
                "model": getattr(self.model, '_model_name', 'gemini-unknown')
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "analysis": None
            }


def main():
    """테스트용 메인 함수"""
    reader = FaceReaderGemini()
    # 실제 사용 예시:
    # result = reader.analyze_face("path/to/face.jpg")
    # print(result)
    print("FaceReaderGemini 클래스가 준비되었습니다.")


if __name__ == "__main__":
    main()
