// API 기본 URL (환경에 따라 자동 감지)
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:8000'  // 로컬 개발 환경
    : window.location.origin;   // 프로덕션 환경 (같은 도메인)

// Kakao SDK 초기화 (발급받은 JavaScript 키로 변경!)
const KAKAO_JS_KEY = '59427f98d8afe38d833c405563436286';

// DOM 요소
const fileInput = document.getElementById('fileInput');
const uploadBox = document.getElementById('uploadBox');
const btnCamera = document.getElementById('btnCamera');
const previewSection = document.getElementById('previewSection');
const previewImage = document.getElementById('previewImage');
const btnRemove = document.getElementById('btnRemove');
const btnAnalyze = document.getElementById('btnAnalyze');
const loadingSection = document.getElementById('loadingSection');
const resultSection = document.getElementById('resultSection');
const analysisResult = document.getElementById('analysisResult');
const btnRetry = document.getElementById('btnRetry');
const btnShareKakao = document.getElementById('btnShareKakao');
const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');
const btnErrorRetry = document.getElementById('btnErrorRetry');
const remainingCount = document.getElementById('remainingCount');

let selectedFile = null;

// 사용 횟수 관리
function getUsageCount() {
    return parseInt(localStorage.getItem('usageCount') || '0');
}

function getBonusCount() {
    return parseInt(localStorage.getItem('bonusCount') || '0');
}

function getRemainingCount() {
    const used = getUsageCount();
    const bonus = getBonusCount();
    return Math.max(0, (1 + bonus) - used);
}

function incrementUsageCount() {
    const current = getUsageCount();
    localStorage.setItem('usageCount', (current + 1).toString());
}

function addBonusCount() {
    const current = getBonusCount();
    localStorage.setItem('bonusCount', (current + 1).toString());
}

function updateRemainingUI() {
    const remaining = getRemainingCount();
    if (remainingCount) {
        remainingCount.textContent = `${remaining}회`;

        if (remaining === 0) {
            remainingCount.style.color = '#EF4444';  // 빨간색
        }
    }
}

// 카카오톡 공유 함수
function shareKakao() {
    if (!window.Kakao) {
        alert('카카오톡 공유 기능을 불러오는 중입니다. 잠시 후 다시 시도해주세요.');
        return;
    }

    Kakao.Share.sendDefault({
        objectType: 'feed',
        content: {
            title: '🔮 AI 얼굴 관상 분석',
            description: '내 관상을 AI가 분석해줬어요! 정말 신기해요! 당신도 해보세요!',
            imageUrl: 'https://via.placeholder.com/800x400.png?text=AI+Face+Reading',  // TODO: 실제 이미지로 변경
            link: {
                mobileWebUrl: window.location.href,
                webUrl: window.location.href
            }
        },
        buttons: [
            {
                title: '내 관상 보러가기',
                link: {
                    mobileWebUrl: window.location.href,
                    webUrl: window.location.href
                }
            }
        ]
    });

    // 공유 완료 처리 (보너스 횟수 추가)
    setTimeout(() => {
        addBonusCount();
        updateRemainingUI();
        alert('✅ 공유 완료! 추가 1회 분석 기회가 제공되었습니다!');
    }, 500);
}

// 초기화
function init() {
    // Kakao SDK 초기화
    if (window.Kakao && !Kakao.isInitialized()) {
        try {
            Kakao.init(KAKAO_JS_KEY);
            console.log('Kakao SDK 초기화 완료');
        } catch (error) {
            console.warn('Kakao SDK 초기화 실패 (키 미설정 또는 잘못된 키)');
        }
    }

    // 남은 횟수 UI 업데이트
    updateRemainingUI();

    // 파일 선택/카메라 버튼 클릭
    btnCamera.addEventListener('click', (e) => {
        e.stopPropagation(); // 이벤트 버블링 방지
        fileInput.click();
    });

    // 업로드 박스 클릭
    uploadBox.addEventListener('click', () => {
        fileInput.click();
    });

    // 파일 선택
    fileInput.addEventListener('change', handleFileSelect);

    // 드래그 앤 드롭
    uploadBox.addEventListener('dragover', handleDragOver);
    uploadBox.addEventListener('dragleave', handleDragLeave);
    uploadBox.addEventListener('drop', handleDrop);

    // 버튼 이벤트
    btnRemove.addEventListener('click', resetUpload);
    btnAnalyze.addEventListener('click', analyzeImage);
    btnRetry.addEventListener('click', resetUpload);
    btnErrorRetry.addEventListener('click', resetUpload);

    // 카카오톡 공유 버튼
    if (btnShareKakao) {
        btnShareKakao.addEventListener('click', shareKakao);
    }
}

// 파일 선택 처리
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        validateAndPreviewFile(file);
    }
}

// 드래그 오버
function handleDragOver(e) {
    e.preventDefault();
    uploadBox.classList.add('dragover');
}

// 드래그 벗어남
function handleDragLeave(e) {
    e.preventDefault();
    uploadBox.classList.remove('dragover');
}

// 드롭
function handleDrop(e) {
    e.preventDefault();
    uploadBox.classList.remove('dragover');

    const file = e.dataTransfer.files[0];
    if (file) {
        validateAndPreviewFile(file);
    }
}

// 파일 검증 및 미리보기
function validateAndPreviewFile(file) {
    // 파일 형식 검증
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
    if (!allowedTypes.includes(file.type)) {
        showError('JPG, PNG, GIF, WEBP 형식의 이미지만 업로드 가능합니다.');
        return;
    }

    // 파일 크기 검증 (10MB 제한)
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
        showError('파일 크기는 10MB를 초과할 수 없습니다.');
        return;
    }

    selectedFile = file;

    // 미리보기 표시
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        uploadBox.style.display = 'none';
        previewSection.style.display = 'block';
    };
    reader.readAsDataURL(file);
}

// 업로드 초기화
function resetUpload() {
    selectedFile = null;
    fileInput.value = '';
    uploadBox.style.display = 'block';
    previewSection.style.display = 'none';
    loadingSection.style.display = 'none';
    resultSection.style.display = 'none';
    errorSection.style.display = 'none';
}

// 이미지 분석
async function analyzeImage() {
    if (!selectedFile) {
        showError('파일을 먼저 선택해주세요.');
        return;
    }

    // 사용 횟수 확인
    if (getRemainingCount() <= 0) {
        showError('분석 횟수를 모두 사용하셨습니다.\n친구에게 공유하면 추가 1회를 받을 수 있어요!');
        return;
    }

    // 로딩 표시
    previewSection.style.display = 'none';
    loadingSection.style.display = 'block';

    try {
        // FormData 생성
        const formData = new FormData();
        formData.append('file', selectedFile);

        // API 호출
        const response = await fetch(`${API_BASE_URL}/api/analyze`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || '분석 중 오류가 발생했습니다.');
        }

        const data = await response.json();

        if (data.success) {
            // 사용 횟수 증가
            incrementUsageCount();
            updateRemainingUI();

            displayResult(data.analysis);
        } else {
            throw new Error(data.error || '분석 결과를 가져올 수 없습니다.');
        }
    } catch (error) {
        console.error('Error:', error);
        showError(error.message || '서버와의 통신 중 오류가 발생했습니다.');
    } finally {
        loadingSection.style.display = 'none';
    }
}

// 결과 표시
function displayResult(analysis) {
    // 분석한 이미지 표시 (previewImage의 src 복사)
    const analyzedImage = document.getElementById('analyzedImage');
    if (analyzedImage && previewImage.src) {
        analyzedImage.src = previewImage.src;
    }

    // 마크다운 스타일 텍스트를 HTML로 변환 (개선된 변환)
    let htmlContent = analysis
        .replace(/\*\*(.*?)\*\*/g, '<h3>$1</h3>') // **제목** -> <h3>
        .replace(/\n\n+/g, '</p><p>') // 여러 줄바꿈 -> 단락 구분
        .replace(/\n/g, '<br>') // 단일 줄바꿈 -> <br>
        .trim(); // 앞뒤 공백 제거

    // 빈 단락 제거
    htmlContent = htmlContent.replace(/<p>\s*<\/p>/g, '');
    htmlContent = htmlContent.replace(/<p>\s*<br>\s*<\/p>/g, '');

    // p 태그로 감싸기
    if (!htmlContent.startsWith('<p>')) {
        htmlContent = '<p>' + htmlContent;
    }
    if (!htmlContent.endsWith('</p>')) {
        htmlContent = htmlContent + '</p>';
    }

    analysisResult.innerHTML = htmlContent;
    resultSection.style.display = 'block';
}

// 에러 표시
function showError(message) {
    errorMessage.textContent = message;
    uploadBox.style.display = 'none';
    previewSection.style.display = 'none';
    loadingSection.style.display = 'none';
    resultSection.style.display = 'none';
    errorSection.style.display = 'block';
}

// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', init);
