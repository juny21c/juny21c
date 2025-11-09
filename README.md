# 🔮 AI 얼굴 관상 분석 서비스

Claude AI Vision을 활용한 얼굴 관상 분석 웹 서비스입니다. 사용자가 얼굴 사진을 업로드하면 AI가 관상을 분석하여 성격, 운세, 특징 등을 해석해줍니다.

## ⚠️ 주의사항

이 서비스는 **재미와 오락을 목적**으로 만들어졌습니다. 관상 분석 결과는 참고용이며 과학적 근거가 없습니다.

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

## 🚀 설치 및 실행

### 1. 저장소 클론

```bash
git clone https://github.com/juny21c/juny21c.git
cd juny21c
```

### 2. 백엔드 설정

#### 환경 변수 설정

```bash
cd backend
cp .env.example .env
```

`.env` 파일을 열고 Anthropic API 키를 입력하세요:

```
ANTHROPIC_API_KEY=your_actual_api_key_here
```

**API 키 발급**: https://console.anthropic.com/

#### Python 가상환경 생성 및 패키지 설치

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt
```

#### 백엔드 서버 실행

```bash
python main.py
```

서버가 `http://localhost:8000`에서 실행됩니다.

### 3. 프론트엔드 실행

간단한 HTTP 서버로 프론트엔드를 실행할 수 있습니다:

```bash
cd ../frontend

# Python 3 내장 서버 사용
python -m http.server 3000
```

브라우저에서 `http://localhost:3000`으로 접속하세요.

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
