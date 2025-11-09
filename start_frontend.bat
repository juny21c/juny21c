@echo off
echo ========================================
echo AI 얼굴 관상 분석 - 웹사이트 시작
echo ========================================
echo.

cd frontend

echo.
echo ========================================
echo 웹사이트를 시작합니다...
echo 잠시 후 브라우저에서 http://localhost:3000 으로 접속하세요!
echo 종료하려면 Ctrl+C를 누르세요.
echo ========================================
echo.

timeout /t 2 /nobreak >nul
start http://localhost:3000

python -m http.server 3000

pause
