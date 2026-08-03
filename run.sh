#!/bin/bash

# 取得當前腳本所在的目錄
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

# 檢查同目錄下是否存在 venv
if [ ! -d "$DIR/venv" ]; then
    echo "錯誤：同目錄下找不到 ./venv！請先執行 ./install.sh"
    exit 1
fi

echo "正在使用同目錄 ./venv 啟動 script.py..."
"$DIR/venv/bin/python3" "$DIR/script.py"