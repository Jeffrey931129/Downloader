import yt_dlp 
import os
import time
import ctypes
import threading
import tkinter as tk
from tkinter import messagebox, filedialog
import tkinter.font as tkFont
from pydub import AudioSegment
import logging

# 設置 DPI 感知
ctypes.windll.shcore.SetProcessDpiAwareness(1)
scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100

# 設置 logging 基本配置
# logging.basicConfig(filename='output.log', level=logging.DEBUG, format='[%(levelname)s] %(message)s (%(asctime)s)')

# 更新進度的回調函數
def progress_hook(d) :
    if d['status'] == 'downloading' :
        percentage = d['_percent_str']
        idx = percentage.find('%')
        if idx != -1 :
            # 去掉 '%' 符號後面空格開始的部分，以及 '%' 符號前面空格以前的部分
            clean_percentage = percentage[idx-5 : idx+1]
            result_label.config(text=f"下載進度 : {clean_percentage}")
    elif d['status'] == 'finished' :
        result_label.config(text="處理中...")

def get_ydl_opts(format) :
    if format == 'mp3' :
        return {
            'format' : 'bestaudio[ext=m4a]/bestaudio',
            'outtmpl' : f'{path_entry.get()}/%(title)s.%(ext)s',
            'ffmpeg_location': 'ffmpeg/bin/ffmpeg.exe',
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
            'outtmpl' : f'{path_entry.get()}/%(title)s.%(ext)s', 
            'ffmpeg_location' : 'ffmpeg/bin/ffmpeg.exe',
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
        ydl_opts = get_ydl_opts(format)
        output_path = path_entry.get()
        info = yt_dlp.YoutubeDL(ydl_opts).extract_info(url, download=False)
        if 'entries' in info :
            titles = [entry['title'] for entry in info['entries']]
        else:
            titles = [info['title']]
        
        for title in titles :
            target_file = f"{output_path}/{title}.{format}"
            # 檢查目標檔案是否存在
            if os.path.exists(target_file) :
                choice = messagebox.askyesno("檔案已存在", f"檔案 '{title}.{format}' 已存在，是否覆蓋？")
                if not choice :
                    result_label.config(text="取消下載")
                    return
                else : 
                    os.remove(target_file)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl :
            ydl.download([url])
            for title in titles :
                target_file = f"{output_path}/{title}.{format}"
                if format == 'mp3' :
                    audio = AudioSegment.from_mp3(target_file)      # ffmpeg 有關?
                    adjusted_audio = audio.apply_gain(-16.33854565016167 - audio.dBFS)  
                    adjusted_audio.export(target_file, format="mp3")
                os.utime(target_file, (time.time(), time.time()))
            result_label.config(text="下載成功")
    except :
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
