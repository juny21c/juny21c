"""
얼굴 관상 분석 모듈
Claude Vision API를 사용하여 얼굴 사진을 분석하고 관상을 해석합니다.
"""

import base64
import os
from typing import Dict, Any
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


class FaceReader:
    """얼굴 관상 분석 클래스"""

    def __init__(self):
        """API 키로 Anthropic 클라이언트 초기화"""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY 환경 변수가 설정되지 않았습니다.")
        self.client = Anthropic(api_key=api_key)

    def encode_image(self, image_path: str) -> tuple[str, str]:
        """
        이미지 파일을 base64로 인코딩

        Args:
            image_path: 이미지 파일 경로

        Returns:
            (base64_data, media_type) 튜플
        """
        with open(image_path, "rb") as image_file:
            image_data = base64.standard_b64encode(image_file.read()).decode("utf-8")

        # 파일 확장자로 미디어 타입 결정
        extension = image_path.lower().split('.')[-1]
        media_type_map = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'webp': 'image/webp'
        }
        media_type = media_type_map.get(extension, 'image/jpeg')

        return image_data, media_type

    def analyze_face(self, image_path: str) -> Dict[str, Any]:
        """
        얼굴 사진을 분석하여 관상을 해석

        Args:
            image_path: 분석할 얼굴 사진 경로

        Returns:
            관상 분석 결과 딕셔너리
        """
        try:
            # 이미지 인코딩
            image_data, media_type = self.encode_image(image_path)

            # Claude Vision API 호출
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": media_type,
                                    "data": image_data,
                                },
                            },
                            {
                                "type": "text",
                                "text": """이 사진 속 사람의 얼굴을 보고 관상을 분석해주세요.

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
                            }
                        ],
                    }
                ],
            )

            # 응답 파싱
            analysis_text = message.content[0].text

            return {
                "success": True,
                "analysis": analysis_text,
                "model": "claude-3-5-sonnet-20241022"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "analysis": None
            }


def main():
    """테스트용 메인 함수"""
    reader = FaceReader()
    # 실제 사용 예시:
    # result = reader.analyze_face("path/to/face.jpg")
    # print(result)
    print("FaceReader 클래스가 준비되었습니다.")


if __name__ == "__main__":
    main()
