#!/bin/bash
set -e

# 取得當前腳本所在的目錄，確保不管在哪裡執行，路徑都鎖定在當前資料夾
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "[1/3] 安裝系統底層需求與 Google Chrome..."
sudo apt update
sudo apt install -y python3-venv python3-pip wget

if ! command -v google-chrome &> /dev/null; then
    wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O /tmp/chrome.deb
    sudo apt install -y /tmp/chrome.deb
    rm /tmp/chrome.deb
fi

echo "[2/3] 在同目錄建立 ./venv 虛擬環境..."
if [ ! -d "$DIR/venv" ]; then
    python3 -m venv "$DIR/venv"
fi

echo "[3/3] 在同目錄 ./venv 中安裝/更新 Selenium..."
"$DIR/venv/bin/pip" install --upgrade pip
"$DIR/venv/bin/pip" install --upgrade selenium

echo "=========================================="
echo "安裝完成！同目錄下的 ./venv 已準備完畢。"
echo "日後請直接執行 ./run.sh"
echo "=========================================="