#!/usr/bin/env python3
"""台北市國小社團自動報名腳本 (Wayland / Linux 專用)"""

from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# ===== 1. 報名個人資訊與課程設定 =====
STUDENT_ID = "YOUR_STUDENT_ID"  # 請替換為你的帳號
PASSWORD = "YOUR_PASSWORD"  # 請替換為你的密碼

# 依優先順序填入目標課程關鍵字（支援模糊匹配，如 "桌球D班" 亦可匹配 "02.桌球D班"）
TARGET_COURSES = ["優先1", "優先2", "優先3", "優先4"]

# ===== 2. 設定搶課啟動時間 (目前設定：12:00:00 啟動) =====
TARGET_HOUR = 12
TARGET_MINUTE = 0
TARGET_SECOND = 0

# ===== 3. 設定 Chrome 瀏覽器 (針對 GNOME Wayland / Headless 最佳化) =====
chrome_options = Options()
# ===== Wayland / Linux 專用無頭模式參數 =====
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--ozone-platform=headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument(
    "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,"
    " like Gecko) Chrome/126.0.0.0 Safari/537.36"
)

driver = webdriver.Chrome(options=chrome_options)


def ensure_frame_context():
  """確保切換到正確的 Frame 框架環境."""
  if len(driver.window_handles) > 1:
    driver.switch_to.window(driver.window_handles[-1])

  frames = driver.find_elements(By.TAG_NAME, "frame") + driver.find_elements(
      By.TAG_NAME, "iframe"
  )
  if len(frames) > 0:
    try:
      driver.switch_to.frame("mainFrame")
    except Exception:
      driver.switch_to.frame(0)


def check_and_handle_warning():
  """處理資格不符或已報名的警告頁面 (input#back)."""
  if "join_class_judge_warning.asp" in driver.current_url:
    print("偵測到警告頁面！點擊 input#back 返回...")
    for _ in range(5):
      try:
        back_btns = driver.find_elements(By.CSS_SELECTOR, "input#back")
        if back_btns:
          driver.execute_script("arguments[0].click();", back_btns[0])
          time.sleep(1)
          ensure_frame_context()
          return True
      except Exception:
        pass
      time.sleep(0.5)
  return False


try:
  # =========================================================
  # 階段 1：預備（進行登入，靜止不點擊任何報名按鈕）
  # =========================================================
  print("[預備] 正在前往登入頁面...")
  driver.get("https://register.shps.tp.edu.tw/login_stu.asp")

  username_input = None
  password_input = None
  for _ in range(15):
    try:
      u_el = driver.find_elements(
          By.XPATH, "//span[contains(text(),'帳號')]/following::input[1]"
      )
      p_el = driver.find_elements(
          By.XPATH, "//span[contains(text(),'密碼')]/following::input[1]"
      )
      if u_el and p_el:
        username_input = u_el[0]
        password_input = p_el[0]
        break
    except Exception:
      pass
    time.sleep(1)

  if username_input and password_input:
    username_input.clear()
    username_input.send_keys("A133014220")
    password_input.clear()
    password_input.send_keys("A133014220")
    print("帳號密碼已填寫完成。")

  # 點擊登入按鈕
  for _ in range(10):
    try:
      btn = driver.find_elements(By.CSS_SELECTOR, "input#kt_login1")
      if btn:
        driver.execute_script("arguments[0].click();", btn[0])
        print("已成功點擊登入！")
        break
    except Exception:
      pass
    time.sleep(1)

  time.sleep(1)
  try:
    alert = driver.switch_to.alert
    alert.accept()
  except Exception:
    pass

  print(f">> 登入準備完畢，進入倒數等待階段 (目標時間 {TARGET_HOUR:02d}:{TARGET_MINUTE:02d}:{TARGET_SECOND:02d})...")

  # =========================================================
  # 階段 2：精確倒數計時，等待至 12:00:00 瞬間
  # =========================================================
  while True:
    now = datetime.now()
    if (
        now.hour > TARGET_HOUR
        or (now.hour == TARGET_HOUR and now.minute > TARGET_MINUTE)
        or (
            now.hour == TARGET_HOUR
            and now.minute == TARGET_MINUTE
            and now.second >= TARGET_SECOND
        )
    ):
      print(
          f"\n[時間到達 {now.strftime('%H:%M:%S')}] 開放時間已到，立即開始搶課！"
      )
      break

    print(
        f"當前時間: {now.strftime('%H:%M:%S')} - 靜止等待中...",
        end="\r",
    )
    time.sleep(0.1)  # 0.1 秒高頻輪詢

  # =========================================================
  # 階段 3：12:00:00 時間到達，執行掃描與報名 (#tab1 ~ #tab6)
  # =========================================================
  base_url = "https://register.shps.tp.edu.tw/class_list_3.asp"
  tabs = [f"#tab{i}" for i in range(1, 7)]

  enrollment_successful = False

  for course_keyword in TARGET_COURSES:
    print(f"\n正在尋找目標課程：【{course_keyword}】...")

    for tab in tabs:
      target_tab_url = f"{base_url}{tab}"
      driver.get(target_tab_url)
      ensure_frame_context()

      # 智慧定位：尋找包含該課程名稱、且可點擊的「報名」按鈕
      smart_xpath = f"//tr[td//a[contains(text(), '{course_keyword}')]]//input[@value='報名' and not(@disabled)]"

      ensure_frame_context()
      buttons = driver.find_elements(By.XPATH, smart_xpath)

      if buttons:
        print(f"在 {tab} 找到『{course_keyword}』！立即點擊報名！")
        driver.execute_script("arguments[0].click();", buttons[0])

        try:
          time.sleep(0.5)
          alert = driver.switch_to.alert
          print(f"提示訊息：{alert.text}")
          alert.accept()
        except Exception:
          pass

        if check_and_handle_warning():
          print(f"『{course_keyword}』無法報名（可能已額滿或已報名），換下一個備用課程...")
          break
        else:
          print(f"『{course_keyword}』報名成功！")
          enrollment_successful = True
          break

    if enrollment_successful:
      break

  if not enrollment_successful:
    print("\n[結果] 嘗試了所有指定課程與分頁，未成功報名新課程。")

  print("\n腳本執行完成。")
  time.sleep(3)

finally:
  driver.quit()
