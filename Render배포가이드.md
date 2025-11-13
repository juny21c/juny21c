# 🚀 Render.com 배포 가이드

60대 여성을 위한 AI 얼굴 관상 분석 서비스를 Render.com에 무료로 배포하는 방법입니다.

## ✅ 준비사항

1. **GitHub 계정** (코드 저장소)
2. **Render.com 계정** (무료 가입)
3. **Google Gemini API 키** (이미 발급 완료: `AIzaSyB...`)
4. **Kakao JavaScript 키** (이미 설정 완료: `59427f...`)

---

## 📋 1단계: GitHub에 코드 푸시

현재 모든 코드가 GitHub 저장소에 있는지 확인하세요.

```bash
git status
git push -u origin claude/face-reading-service-011CUwotHqDfP6wWf7eZCbG6
```

**중요:** 메인 브랜치로 Pull Request를 만들고 머지하세요!

---

## 🌐 2단계: Render.com 회원가입 및 연동

### 1. Render.com 가입
1. https://render.com 접속
2. **"Get Started for Free"** 클릭
3. **GitHub 계정으로 가입** (권장)

### 2. 저장소 연결
1. Render 대시보드에서 **"New +"** 클릭
2. **"Web Service"** 선택
3. GitHub 저장소 연결 권한 허용
4. **juny21c/juny21c** 저장소 선택

---

## ⚙️ 3단계: 서비스 설정

### 기본 설정

| 항목 | 값 |
|------|-----|
| **Name** | `face-reading-service` (원하는 이름) |
| **Region** | `Singapore` (한국과 가까움) |
| **Branch** | `main` (또는 메인 브랜치 이름) |
| **Root Directory** | 비워두기 |
| **Runtime** | `Python 3` |

### Build & Start 설정

| 항목 | 명령어 |
|------|--------|
| **Build Command** | `cd backend && pip install -r requirements.txt` |
| **Start Command** | `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT` |

### 환경 변수 설정

**"Advanced"** → **"Add Environment Variable"** 클릭 후 추가:

| Key | Value |
|-----|-------|
| `API_PROVIDER` | `gemini` |
| `GOOGLE_API_KEY` | `AIzaSyBvPcz8zoKoR6B4BRUuTyDYpKPSJn2cL5Q` |
| `PYTHON_VERSION` | `3.11.0` |

**⚠️ 주의:** API 키는 비공개로 설정하세요!

---

## 🎯 4단계: 배포 시작

1. **"Create Web Service"** 클릭
2. 자동으로 배포 시작 (5-10분 소요)
3. 배포 로그에서 진행 상황 확인

✅ 성공 메시지:
```
🌟 Google Gemini API를 사용합니다
INFO: Uvicorn running on http://0.0.0.0:10000
```

---

## 🌍 5단계: 서비스 URL 확인

배포 완료 후 상단에 URL이 나타납니다:
```
https://face-reading-service.onrender.com
```

이 URL을 브라우저에서 열면 바로 서비스 사용 가능! 🎉

---

## 🔧 6단계: 커스텀 도메인 설정 (선택사항)

무료 플랜에서도 커스텀 도메인 사용 가능합니다!

### 도메인 구매 (예: Namecheap, GoDaddy, Gabia)
1. 원하는 도메인 구매 (예: `face-reading.com`)
2. DNS 설정에서 CNAME 레코드 추가:
   - **Name:** `www` 또는 `@`
   - **Value:** `face-reading-service.onrender.com`

### Render에서 설정
1. 서비스 설정 → **"Custom Domain"** 클릭
2. 구매한 도메인 입력
3. SSL 인증서 자동 발급 (무료!)

---

## 📱 7단계: 카카오톡 공유 설정

실제 도메인을 받았으면 카카오 개발자 콘솔 업데이트:

1. https://developers.kakao.com 접속
2. 내 애플리케이션 → 플랫폼 설정
3. **Web 플랫폼 추가:**
   - `https://face-reading-service.onrender.com` (Render URL)
   - 또는 커스텀 도메인

이제 카카오톡 공유가 정상 작동합니다! 💬

---

## 🎨 8단계: 공유 이미지 변경 (선택사항)

더 멋진 공유 화면을 위해 이미지를 업로드하세요:

1. 대표 이미지 제작 (800x400px 권장)
2. 무료 이미지 호스팅 (Imgur, Cloudinary 등)
3. `frontend/script.js` 75번째 줄 수정:
```javascript
imageUrl: 'https://your-image-url.com/face-reading.png',
```

---

## 💰 9단계: Google AdSense 설정

트래픽이 발생하면 AdSense 신청:

1. https://www.google.com/adsense 접속
2. 사이트 URL 등록 (Render 또는 커스텀 도메인)
3. 승인 후 광고 코드를 `frontend/index.html`에 추가

**수익 발생 시작!** 💵

---

## 📊 10단계: YouTube 홍보 준비

36,000명 구독자 채널에서 홍보:

### 영상 준비
1. **썸네일:** "AI 관상 분석" + 신비로운 이미지
2. **제목:** "AI가 내 얼굴 보고 관상 분석해줬어요!"
3. **설명란:**
   ```
   🔮 무료 AI 얼굴 관상 분석
   👉 https://face-reading-service.onrender.com

   친구에게 공유하면 1회 더! 💬
   ```

### 고정 댓글
```
📱 여러분도 해보세요!
링크: https://face-reading-service.onrender.com
공유하면 1회 더 받을 수 있어요! 😊
```

---

## ⚡ 무료 플랜 제한사항

| 항목 | 제한 |
|------|------|
| **비활성 시** | 15분 후 슬립 모드 (첫 접속 느림) |
| **월 사용 시간** | 750시간/월 (충분함!) |
| **대역폭** | 100GB/월 |
| **메모리** | 512MB |

**💡 팁:** 자주 사용되면 슬립 모드 없음!

---

## 🔄 업데이트 방법

코드 수정 후:

```bash
git add .
git commit -m "업데이트 내용"
git push
```

Render가 **자동으로 재배포**합니다! 🚀

---

## 🆘 문제 해결

### 1. 배포 실패 시
- Render 대시보드에서 **Logs** 확인
- Build Command와 Start Command 재확인
- 환경 변수 올바르게 입력되었는지 확인

### 2. API 오류 시
- `GOOGLE_API_KEY`가 올바른지 확인
- Google AI Studio에서 API 할당량 확인 (1,500회/일)

### 3. 카카오톡 공유 안 될 때
- 카카오 개발자 콘솔에서 도메인 등록 확인
- JavaScript 키가 올바른지 확인

---

## 🎯 성공 체크리스트

- [ ] Render.com에 배포 완료
- [ ] 서비스 URL 접속 가능
- [ ] 사진 업로드 및 분석 작동
- [ ] 사용 횟수 카운트 작동
- [ ] 카카오톡 공유 버튼 작동 (실제 도메인)
- [ ] YouTube 영상 업로드 준비
- [ ] AdSense 신청 (트래픽 발생 후)

---

## 📞 지원

문제가 있으면 Render 지원팀에 문의하거나, GitHub Issues를 활용하세요!

**연말 전 성공적인 런칭을 응원합니다! 🎉**
