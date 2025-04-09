@echo off
echo.
echo 🔧 Gerekli Python kutuphaneleri yukleniyor...
echo.

REM Eğer requirements.txt varsa onu kullan
IF EXIST requirements.txt (
    pip install -r requirements.txt
) ELSE (
    pip install discord.py pymongo
)

echo.
echo ✅ Kurulum tamamlandi!
pause
