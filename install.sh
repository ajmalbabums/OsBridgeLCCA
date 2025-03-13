#!/bin/bash

ENV_NAME="osbridge-lcca"

echo "🔍 Checking for Conda installation..."
if ! command -v conda &> /dev/null; then
    echo "❌ Conda not found! Please install Miniconda/Anaconda first."
    exit 1
fi

echo "✅ Conda found! Creating Conda environment: $ENV_NAME"
conda create -y -n $ENV_NAME python=3.10 flask pyqt plotly pylatex numpy pandas matplotlib requests pytest pytest-qt

echo "🔄 Activating Conda environment..."
source activate $ENV_NAME || conda activate $ENV_NAME

echo "📦 Installing additional pip dependencies..."
pip install -r requirements.txt

echo "✅ Installation complete! Running verification..."
python tests/verify_installation.py
