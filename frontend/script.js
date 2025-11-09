// API 기본 URL (개발 환경에 맞게 수정)
const API_BASE_URL = 'http://localhost:8000';

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
const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');
const btnErrorRetry = document.getElementById('btnErrorRetry');

let selectedFile = null;

// 초기화
function init() {
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
    // 마크다운 스타일 텍스트를 HTML로 변환 (간단한 변환)
    let htmlContent = analysis
        .replace(/\*\*(.*?)\*\*/g, '<h3>$1</h3>') // **제목** -> <h3>
        .replace(/\n\n/g, '</p><p>') // 단락 구분
        .replace(/\n/g, '<br>'); // 줄바꿈

    htmlContent = '<p>' + htmlContent + '</p>';

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
