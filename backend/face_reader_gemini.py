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
            # 이미지 로드 및 최적화
            image = Image.open(image_path)

            # 이미지 리사이즈 (512px max) - 속도 최적화
            max_size = 512
            if image.width > max_size or image.height > max_size:
                image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                print(f"✅ 이미지 리사이즈: {image.width}x{image.height}")

            # RGB 모드로 변환 (투명도 제거)
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # 프롬프트 생성 (간결하게 최적화)
            prompt = """당신은 30년 경력 관상가입니다. 이 얼굴을 보고 간결하게 풀이해주세요.

**성격과 기질**
타고난 성품과 특징 (2줄)

**재물운**
금전, 사업운과 조언 (2줄)

**인간관계운**
대인관계, 인복 (2줄)

**건강과 활력**
건강 상태와 주의점 (1-2줄)

**종합 운세**
전반적 운세와 삶의 조언 (2-3줄, 희망적으로)

간결하고 구체적으로, 따뜻한 어조로 작성하세요."""

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

            # 생성 설정 (속도 최적화)
            generation_config = {
                "max_output_tokens": 600,  # 짧게 제한
                "temperature": 0.7,  # 약간 창의적
            }

            response = self.model.generate_content(
                [prompt, image],
                safety_settings=safety_settings,
                generation_config=generation_config
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
