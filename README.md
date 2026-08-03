# school_auto
自動搶社團
## 安裝與執行說明

### 1. 初次安裝環境
在終端機切換至專案目錄，並執行安裝腳本（會自動在同目錄下建立 `./venv` 並安裝依賴）：

```bash
chmod +x install.sh run.sh
./install.sh
```
## 腳本設定

在執行前，請先編輯 `script.py` 中的個人資訊與報名目標：

```python
# 填入學號與密碼（請保留雙引號）
STUDENT_ID = "YOUR_STUDENT_ID"
PASSWORD = "YOUR_PASSWORD"

# 依優先順序填入目標課程關鍵字（支援模糊比對）
TARGET_COURSES = [
    "02.桌球D班",
    "桌球D班",
    "羽球班",
    "英文1A班"
]
```
Scripted by Gemini Tested by Me
