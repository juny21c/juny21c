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
        # gemini-1.5-flash 사용 (suffix 없이)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

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

            # 프롬프트 생성
            prompt = """이 사진 속 사람의 얼굴을 보고 관상을 분석해주세요.

다음 항목들을 포함하여 자세하고 긍정적으로 분석해주세요:

1. **전체적인 인상**: 얼굴형, 전반적인 느낌
2. **이마와 눈썹**: 지혜, 사고력, 리더십 관련
3. **눈**: 성격, 감성, 통찰력 관련
4. **코**: 재물운, 의지력 관련
5. **입과 턱**: 언변, 인간관계, 생활력 관련
6. **귀**: 복, 수명, 지혜 관련
7. **전체적인 운세**: 종합적인 해석과 조언

각 항목마다 구체적이고 긍정적인 해석을 제공하되, 너무 과장되지 않도록 균형잡힌 시각으로 작성해주세요.
한국어로 친근하고 이해하기 쉽게 설명해주세요."""

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
                "model": "gemini-1.5-flash"
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
