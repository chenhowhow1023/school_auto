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
# ===== 1. 報名個人資訊與課程設定 =====
STUDENT_ID = "YOUR_STUDENT_ID"  # 請替換為你的帳號
PASSWORD = "YOUR_PASSWORD"  # 請替換為你的密碼

# 依優先順序填入目標課程關鍵字（支援模糊匹配，如 "桌球D班" 亦可匹配 "02.桌球D班"）
TARGET_COURSES = ["優先1", "優先2", "優先3", "優先4"]
```
Scripted by Gemini Tested by Me
