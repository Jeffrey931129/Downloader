import yt_dlp 
import os
import json
import shutil
import time
from datetime import datetime
import ctypes
import threading
import tkinter as tk
from tkinter import messagebox, filedialog
import tkinter.font as tkFont
from pydub import AudioSegment

# 設置 DPI 感知
ctypes.windll.shcore.SetProcessDpiAwareness(1)
scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
AudioSegment.ffmpeg = "ffmpeg/bin/ffmpeg.exe"
cookie_file = "cookie.txt"          # ?

# 更新進度的回調函數
def progress_hook(d) :
    if d['status'] == 'downloading' :
        # with open("test.txt", 'a') as file :          # Debug
        #     json.dump(d, file, indent=4)
        #     file.write("\n")
        total_bytes = d.get('total_bytes')
        total_fragment = d.get('fragment_count')
        if total_bytes :
            result_label.config(text=f"下載進度 : {(d['downloaded_bytes'] / total_bytes * 100):.2f}%")
        elif total_fragment :
            result_label.config(text=f"下載進度 : {(d['fragment_index'] / total_fragment * 100):.2f}%")

def get_ydl_opts(output_path, dir_name, format) :
    if format == 'mp3' :
        return {
            'format' : 'bestaudio[ext=m4a]/bestaudio',
            'outtmpl' : f'{output_path}/{dir_name}/%(title)s.%(ext)s',
            'ffmpeg_location': 'ffmpeg/bin/ffmpeg.exe',
            # 'cookiefile': cookie_file,            # 需要時看看他的錯誤訊息，然後依此偵測抓取新的 cookie (for future)
            'http_headers' : {
                'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            },
            'postprocessors' : [{
                'key' : 'FFmpegExtractAudio',
                'preferredcodec' : format,
                'preferredquality' : '192',
            }],
            'progress_hooks' : [progress_hook]
        }
    else :
        return {
            'format' : 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',  
            'outtmpl' : f'{output_path}/{dir_name}/%(title)s.%(ext)s', 
            'ffmpeg_location' : 'ffmpeg/bin/ffmpeg.exe',
            # 'cookiefile': cookie_file,
            'http_headers' : {
                'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            },
            'postprocessors' : [{
                'key' : 'FFmpegVideoConvertor',
                'preferedformat' : 'mp4',  
            }],
            'progress_hooks': [progress_hook]
        }

def download_video(url, format) :
    try :
        dir_name = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H-%M-%S')    # 以時間作為資料夾名稱
        output_path = path_entry.get()
        os.makedirs(f"{output_path}/{dir_name}", exist_ok=True)
        ydl_opts = get_ydl_opts(output_path, dir_name, format)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl :
            ydl.download([url])
            result_label.config(text="處理中...")
            for filename in os.listdir(f"{output_path}/{dir_name}") :
                if format == 'mp3' :
                    audio = AudioSegment.from_mp3(f"{output_path}/{dir_name}/{filename}")     # 與 ffmpeg 有關?
                    adjusted_audio = audio.apply_gain(-16.33854565016167 - audio.dBFS)  
                    adjusted_audio.export(f"{output_path}/{dir_name}/{filename}", format="mp3")
                os.utime(f"{output_path}/{dir_name}/{filename}", (time.time(), time.time()))
                shutil.move(f"{output_path}/{dir_name}/{filename}", f"{output_path}/{filename}")
            shutil.rmtree(f"{output_path}/{dir_name}")
            result_label.config(text="下載成功")
    except Exception as exception :
        result_label.config(text="下載失敗")

def on_select_directory() :
    # 打開文件夾選擇對話框
    directory = filedialog.askdirectory()
    if directory :
        # 更新顯示選擇的儲存路徑
        path_entry.delete(0, tk.END)  # 清空現有內容
        path_entry.insert(0, directory)  # 插入新內容
        with open("output_path.txt", 'w') as file :
            file.write(directory)

def on_download_button_click() :
    url = url_entry.get()
    format = format_var.get()
    if url :
        result_label.config(text="下載中...")
        # 使用執行緒執行下載任務
        download_thread = threading.Thread(target=download_video, args=(url, format))
        download_thread.start()
    else :
        messagebox.showwarning("輸入錯誤", "請輸入 YouTube 網址")

# init
root = tk.Tk()
root.title("YouTube 下載器")
root.geometry(f"400x270+{int(root.winfo_screenwidth()/2*1.3)}+100")
root.iconbitmap('music.ico')
root.wm_attributes("-topmost", 1)       # 設置窗口為最上層
custom_font = tkFont.Font(family="DFKai-SB", size=int(12), weight="bold")
# -------------------------------------------------------------------------------------------

# url
url_label = tk.Label(root, text="請輸入 YouTube 網址 : ", font=custom_font)
url_label.place(x=200, y=30, anchor="center")

url_entry = tk.Entry(root)
url_entry.place(x=10, y=70, anchor="w", width=380)
# -------------------------------------------------------------------------------------------

# path
path_label = tk.Label(root, text="儲存位置 : ", font=custom_font)
path_label.place(x=200, y=110, anchor="center")

path_entry = tk.Entry(root)
path_entry.place(x=10, y=150, anchor="w", width=335)

path_button = tk.Button(root, text="...", command=on_select_directory, font=custom_font)
path_button.place(x=370, y=150, anchor="center", width=40, height=25)
with open("output_path.txt", 'r') as file :
    directory = file.read().strip()
    path_entry.delete(0, tk.END)  # 清空現有內容
    path_entry.insert(0, directory)  # 插入新內容
# -------------------------------------------------------------------------------------------

# format
format_options = ['mp3', 'mp4']
format_var = tk.StringVar(value='mp3')
format_menu = tk.OptionMenu(root, format_var, *format_options)
format_menu.config(font=custom_font)
format_menu.place(x=150, y=200, anchor="center", height=40)
# -------------------------------------------------------------------------------------------

# download
download_button = tk.Button(root, text="下載", command=on_download_button_click, font=custom_font)
download_button.place(x=250, y=200, anchor="center", height=40)
# -------------------------------------------------------------------------------------------

# result
result_label = tk.Label(root, text="", font=custom_font)
result_label.place(x=200, y=245, anchor="center")
# -------------------------------------------------------------------------------------------

# mainloop
root.mainloop()
