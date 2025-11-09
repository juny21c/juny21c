#!/bin/bash

echo "========================================"
echo "AI 얼굴 관상 분석 - 백엔드 서버 시작"
echo "========================================"
echo ""

cd backend

echo "API 키를 확인하는 중..."
if [ ! -f .env ]; then
    echo "[오류] .env 파일이 없습니다!"
    echo ""
    echo ".env.example 파일을 복사해서 .env 파일을 만들고"
    echo "ANTHROPIC_API_KEY를 설정해주세요."
    echo ""
    read -p "계속하려면 Enter를 누르세요..."
    exit 1
fi

echo "필요한 패키지를 확인하는 중..."
if ! pip show fastapi &> /dev/null; then
    echo "필요한 패키지를 설치하는 중... 잠시만 기다려주세요."
    pip install -r requirements.txt
fi

echo ""
echo "========================================"
echo "서버를 시작합니다..."
echo "브라우저에서 http://localhost:3000 으로 접속하세요!"
echo "종료하려면 Ctrl+C를 누르세요."
echo "========================================"
echo ""

python main.py
