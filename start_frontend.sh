#!/bin/bash

echo "========================================"
echo "AI 얼굴 관상 분석 - 웹사이트 시작"
echo "========================================"
echo ""

cd frontend

echo ""
echo "========================================"
echo "웹사이트를 시작합니다..."
echo "브라우저에서 http://localhost:3000 으로 접속하세요!"
echo "종료하려면 Ctrl+C를 누르세요."
echo "========================================"
echo ""

# Mac에서 브라우저 자동으로 열기
if [[ "$OSTYPE" == "darwin"* ]]; then
    sleep 2
    open http://localhost:3000
fi

# Linux에서 브라우저 자동으로 열기
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sleep 2
    xdg-open http://localhost:3000 2>/dev/null
fi

python3 -m http.server 3000
