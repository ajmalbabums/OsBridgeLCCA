@echo off
SET ENV_NAME=osbridge-lcca

echo Checking for Conda installation...
where conda >nul 2>nul
IF ERRORLEVEL 1 (
    echo ❌ Conda not found! Please install Miniconda/Anaconda first.
    exit /b 1
)

echo ✅ Conda found! Creating Conda environment: %ENV_NAME%
call conda create -y -n %ENV_NAME% python=3.10 flask pyqt plotly pylatex numpy pandas matplotlib requests pytest pytest-qt

echo 🔄 Activating Conda environment...
call conda activate %ENV_NAME%

echo 📦 Installing additional pip dependencies...
pip install -r requirements.txt

echo ✅ Installation complete! Running verification...
python tests\verify_installation.py
