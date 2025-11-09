"""
얼굴 관상 분석 - Hugging Face Spaces 버전
Gradio를 사용한 간단한 웹 인터페이스
"""

import os
import gradio as gr
from PIL import Image
import google.generativeai as genai

# Hugging Face Secrets에서 API 키 가져오기
# 로컬 테스트시에는 환경변수에서 가져옴
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY가 설정되지 않았습니다. Hugging Face Spaces의 Settings > Repository secrets에서 설정해주세요.")

# Gemini 설정
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 관상 분석 함수
def analyze_face(image):
    """
    업로드된 이미지를 분석하여 관상 결과 반환
    """
    if image is None:
        return "⚠️ 사진을 먼저 업로드해주세요!"

    try:
        # PIL Image로 변환 (Gradio가 numpy array로 전달할 수 있음)
        if not isinstance(image, Image.Image):
            image = Image.fromarray(image)

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

        # Gemini API 호출
        response = model.generate_content([prompt, image])

        return response.text

    except Exception as e:
        return f"❌ 오류가 발생했습니다: {str(e)}\n\n다시 시도해주세요."

# Gradio 인터페이스 구성
def create_interface():
    with gr.Blocks(title="🔮 AI 얼굴 관상 분석", theme=gr.themes.Soft()) as demo:
        gr.Markdown(
            """
            # 🔮 AI 얼굴 관상 분석 서비스

            얼굴 사진을 업로드하면 AI가 관상을 분석해드립니다!

            ⚠️ **주의**: 이 서비스는 재미와 오락을 목적으로 만들어졌습니다.
            관상 분석 결과는 참고용이며 과학적 근거가 없습니다.
            """
        )

        with gr.Row():
            with gr.Column(scale=1):
                image_input = gr.Image(
                    label="📸 얼굴 사진 업로드",
                    type="pil",
                    height=400
                )
                analyze_button = gr.Button(
                    "🔮 관상 분석하기",
                    variant="primary",
                    size="lg"
                )

                gr.Markdown(
                    """
                    ### 💡 사용 팁
                    - 명확한 얼굴이 나온 사진이 좋아요
                    - 정면 사진을 권장합니다
                    - JPG, PNG 형식 지원
                    """
                )

            with gr.Column(scale=1):
                result_output = gr.Textbox(
                    label="📊 관상 분석 결과",
                    lines=20,
                    placeholder="사진을 업로드하고 '관상 분석하기' 버튼을 눌러주세요...",
                )

        # 버튼 클릭 이벤트
        analyze_button.click(
            fn=analyze_face,
            inputs=image_input,
            outputs=result_output
        )

        gr.Markdown(
            """
            ---
            ### 📝 안내사항
            - 이 서비스는 Google Gemini AI를 사용합니다
            - 업로드된 사진은 저장되지 않습니다
            - 재미로만 봐주세요! 🎉

            Made with ❤️ by @juny21c
            """
        )

    return demo

# 앱 실행
if __name__ == "__main__":
    demo = create_interface()
    demo.launch()
