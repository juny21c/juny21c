# 🔮 AI 얼굴 관상 분석 서비스

얼굴 사진을 업로드하면 AI가 관상을 봐주는 재미있는 웹사이트입니다!

> 🎓 **완전 초보자이신가요?** [초보자 가이드](./초보자_가이드.md)를 먼저 읽어보세요!

## ⚠️ 이것은 재미로만 봐주세요!

이 서비스는 **재미와 오락 목적**으로 만들어졌습니다. 관상 분석 결과는 참고용이며 과학적 근거가 없어요.

---

## 🎯 이 프로그램이 뭐하는 건가요?

1. 여러분의 얼굴 사진을 업로드하면
2. AI가 얼굴을 보고 관상을 분석해서
3. 이마, 눈, 코, 입, 귀 등을 보고 성격이나 운세를 재미로 알려줍니다!

마치 관상가를 만나는 것처럼요 😊

## ✨ 주요 기능

- 얼굴 사진 업로드 (드래그 앤 드롭 지원)
- AI 기반 얼굴 관상 분석
- 다양한 관상 요소 해석 (이마, 눈, 코, 입, 귀 등)
- 직관적이고 아름다운 웹 인터페이스

## 🛠️ 기술 스택

### 백엔드
- **FastAPI**: 고성능 Python 웹 프레임워크
- **Anthropic Claude API**: AI Vision 기반 이미지 분석
- **Python 3.8+**

### 프론트엔드
- **HTML5/CSS3**: 반응형 웹 디자인
- **JavaScript (Vanilla)**: 동적 인터랙션
- **Fetch API**: 비동기 통신

## 📁 프로젝트 구조

```
juny21c/
├── backend/              # 백엔드 서버
│   ├── main.py          # FastAPI 메인 서버
│   ├── face_reader.py   # 관상 분석 로직
│   ├── requirements.txt # Python 패키지 의존성
│   └── .env.example     # 환경 변수 예시
├── frontend/            # 프론트엔드 웹
│   ├── index.html       # 메인 HTML
│   ├── style.css        # 스타일시트
│   └── script.js        # JavaScript 로직
├── .gitignore
└── README.md
```

## 🚀 어떻게 실행하나요? (완전 초보자용 가이드)

### 필요한 것들

1. **Python 설치** (컴퓨터에 Python이 있어야 해요)
   - Windows: https://www.python.org/downloads/ 에서 다운로드
   - 설치할 때 "Add Python to PATH" 체크박스 꼭 선택하세요!

2. **AI API 키** (둘 중 하나만 선택하세요!)

   **🌟 옵션 1: Google Gemini (무료, 초보자 추천!)**
   - https://aistudio.google.com/app/apikey 에서 무료로 발급
   - 구글 계정으로 로그인만 하면 바로 사용 가능!
   - 매달 무료 할당량 제공

   **💎 옵션 2: Anthropic Claude (유료, 더 정확함)**
   - https://console.anthropic.com/ 에서 가입
   - 사용량에 따라 요금 발생

### 실행 방법

#### 🌟 방법 1: 더블클릭으로 간편 실행 (추천!)

API 키만 설정하면 파일을 더블클릭해서 실행할 수 있어요!

**Windows 사용자:**
1. `start_backend.bat` 더블클릭 (백엔드 서버 시작)
2. `start_frontend.bat` 더블클릭 (웹사이트 시작)

**Mac/Linux 사용자:**
1. 터미널에서: `./start_backend.sh` (백엔드 서버 시작)
2. 새 터미널에서: `./start_frontend.sh` (웹사이트 시작)

끝! 브라우저가 자동으로 열려요! 🎉

> 💡 **처음 실행하는 경우**: 먼저 아래 "방법 2"의 1~2단계를 먼저 해주세요 (코드 다운로드 + API 키 설정)

---

#### 📝 방법 2: 단계별 실행 (직접 명령어 입력)

좀 더 자세히 알고 싶으신 분들을 위해!

**1단계: 코드 다운로드**

컴퓨터의 원하는 폴더에서 명령 프롬프트(CMD) 또는 터미널을 열고:

```bash
git clone https://github.com/juny21c/juny21c.git
cd juny21c
```

> **git이 없다고 나오면?** 그냥 GitHub에서 ZIP 파일로 다운받아서 압축 푸세요!

#### 2단계: API 키 설정

`backend` 폴더로 들어가서:

```bash
cd backend
```

그리고 `.env.example` 파일을 복사해서 `.env` 파일을 만들어요:

**Windows:**
```bash
copy .env.example .env
```

**Mac/Linux:**
```bash
cp .env.example .env
```

그 다음 `.env` 파일을 메모장으로 열고, 사용할 AI를 선택하세요:

**🌟 Google Gemini 사용 (무료, 추천!):**
```
API_PROVIDER=gemini
GOOGLE_API_KEY=여기에_복사한_Gemini_API_키_붙여넣기
```

**💎 Anthropic Claude 사용 (유료):**
```
API_PROVIDER=claude
ANTHROPIC_API_KEY=여기에_복사한_Claude_API_키_붙여넣기
```

저장하고 닫기!

#### 3단계: 필요한 프로그램 설치

같은 폴더(`backend`)에서:

```bash
pip install -r requirements.txt
```

> 이 명령어는 프로그램이 작동하는데 필요한 것들을 자동으로 설치해줘요.
> 조금 시간이 걸릴 수 있어요 (1-2분)

#### 4단계: 서버 실행!

이제 서버를 켜요:

```bash
python main.py
```

이런 메시지가 나오면 성공! 🎉
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

> **주의**: 이 창은 닫지 마세요! 서버가 계속 실행되고 있어야 해요.

#### 5단계: 웹사이트 열기

**새로운** 명령 프롬프트/터미널 창을 하나 더 열고:

```bash
cd juny21c/frontend
python -m http.server 3000
```

#### 6단계: 브라우저에서 접속

인터넷 브라우저(크롬, 엣지 등)를 열고 주소창에:

```
http://localhost:3000
```

입력하고 엔터! 이제 사진을 업로드해서 관상을 봐보세요! 📸

### 🛑 종료하는 방법

두 개의 명령 프롬프트 창에서 각각 `Ctrl + C`를 누르면 프로그램이 종료돼요.

## 📖 사용 방법

1. 웹 브라우저에서 프론트엔드 URL 접속
2. 얼굴 사진을 선택하거나 드래그 앤 드롭
3. "관상 분석하기" 버튼 클릭
4. AI가 분석한 관상 결과 확인

## 🔌 API 엔드포인트

### `GET /`
API 상태 확인

### `GET /health`
헬스 체크

### `POST /api/analyze`
얼굴 사진 분석

**요청**:
- Method: POST
- Content-Type: multipart/form-data
- Body: `file` (이미지 파일)

**응답**:
```json
{
  "success": true,
  "analysis": "관상 분석 결과 텍스트...",
  "model": "claude-3-5-sonnet-20241022"
}
```

### `DELETE /api/cleanup`
임시 업로드 파일 정리

## 🎨 지원하는 이미지 형식

- JPG/JPEG
- PNG
- GIF
- WEBP

최대 파일 크기: 10MB

## 🔧 개발

### 백엔드 개발 서버

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 코드 구조

- `backend/main.py`: FastAPI 라우트 및 파일 업로드 처리
- `backend/face_reader.py`: Claude Vision API를 통한 관상 분석
- `frontend/script.js`: 프론트엔드 로직 및 API 통신

## 🤝 기여

이슈와 풀 리퀘스트를 환영합니다!

## 📝 라이선스

이 프로젝트는 개인 학습 및 재미 목적으로 만들어졌습니다.

## 👤 개발자

**@juny21c**
- 관심 분야: Optimization, Data Visualization, Data Analytics

---

**재미로 즐기세요! 🎉**
