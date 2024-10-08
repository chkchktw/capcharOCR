# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
from PIL import Image
import pytesseract
import subprocess
from io import BytesIO
import os

# 指定 Tesseract OCR 執行檔的路徑
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def perform_ocr():
    url = url_entry.get()
    
    try:
        # 使用 curl 下載圖片
        result = subprocess.run(['curl', '-k', '-L', url], capture_output=True, check=True)
        image_data = result.stdout
        
        # 將下載的數據轉換為圖片
        captcha_image = Image.open(BytesIO(image_data))
        
        # 進行 OCR
        captcha_text = pytesseract.image_to_string(captcha_image, lang='eng+chi_tra')
        captcha_text = captcha_text.strip().replace(" ", "")
        
        # 顯示結果
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, captcha_text)
        result_text.configure(font=("Arial", 30))
        result_text.config(state=tk.DISABLED)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("錯誤", f"下載圖片失敗: {e}")
    except pytesseract.TesseractNotFoundError:
        messagebox.showerror("錯誤", f"無法找到Tesseract OCR。請確認安裝路徑：{pytesseract.pytesseract.tesseract_cmd}")
    except pytesseract.TesseractError as e:
        messagebox.showerror("Tesseract錯誤", f"OCR處理錯誤: {e}")
    except Exception as e:
        messagebox.showerror("錯誤", f"未預期的錯誤: {e}\n"
                                    f"Tesseract 路徑: {pytesseract.pytesseract.tesseract_cmd}")

# 檢查 curl 是否可用
def check_curl():
    try:
        subprocess.run(['curl', '--version'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        messagebox.showerror("錯誤", "未找到curl。請確保curl已安裝並添加到系統PATH中。")
        return False
    return True

# 創建主視窗
window = tk.Tk()
window.title("OCR程式")
window.geometry("400x300")

# 創建網址輸入框
url_label = ttk.Label(window, text="請輸入網址:")
url_label.pack(pady=10)
url_entry = ttk.Entry(window, width=40)
url_entry.pack()

# 創建按鈕觸發OCR
ocr_button = ttk.Button(window, text="執行OCR", command=perform_ocr)
ocr_button.pack(pady=10)

# 創建顯示OCR結果的文本框
result_label = ttk.Label(window, text="OCR結果:")
result_label.pack()
result_text = scrolledtext.ScrolledText(window, width=40, height=5, font=("Arial", 30), state=tk.DISABLED)
result_text.pack(pady=10)

# 檢查必要的組件
if not check_curl():
    ocr_button.config(state=tk.DISABLED)

if not os.path.exists(pytesseract.pytesseract.tesseract_cmd):
    messagebox.showwarning("警告", f"找不到Tesseract OCR執行檔：{pytesseract.pytesseract.tesseract_cmd}\n請確認安裝路徑是否正確。")

# 啟動主迴圈
window.mainloop()
