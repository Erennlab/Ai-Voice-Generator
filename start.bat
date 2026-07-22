@echo off
title Seslendirici Başlatıcı
echo ===================================================
echo   YAPAY ZEKA SESLENDİRİCİ SİSTEMİ BAŞLATILIYOR...
echo ===================================================
echo.

echo [1/2] API Sunucusu Başlatılıyor...
start "Seslendirici Sunucu" cmd /k "python -m uvicorn server:app --host 127.0.0.1 --port 8000"

echo [2/2] Arayüz Açılıyor...
timeout /t 2 /nobreak >nul
start index.html

echo.
echo ===================================================
echo   Sistem Başlatıldı! Sunucu penceresini kapatmayın.
echo ===================================================
pause
