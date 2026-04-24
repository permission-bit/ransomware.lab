# ================================
# Windows Build Script (PowerShell)
# ================================

Write-Host "Cleaning old builds..." -ForegroundColor Yellow

# Alte Builds löschen
Remove-Item -Recurse -Force build, dist, *.spec -ErrorAction SilentlyContinue

Write-Host "Creating virtual environment..." -ForegroundColor Yellow

# Venv erstellen (Python 3.11 empfohlen)
python -m venv venv

# Venv aktivieren
.\venv\Scripts\Activate.ps1

Write-Host "Installing requirements..." -ForegroundColor Yellow

# Dependencies installieren
pip install --upgrade pip
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
}

Write-Host "Building application..." -ForegroundColor Green

# PyInstaller Build (GUI ohne Konsole)
pyinstaller `
    --noconfirm `
    --clean `
    --windowed `
    --name "software" `
    --icon "icon.ico" `
    software.py

Write-Host "Build finished!" -ForegroundColor Green

# Optional: dist öffnen
#Start-Process explorer.exe ".\dist"