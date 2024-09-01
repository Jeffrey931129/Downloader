import subprocess
import os
import shutil

# 使用列表格式來傳遞參數
subprocess.run([
    "pyinstaller",
    "--onefile",
    "--windowed",
    "--icon=music.ico",
    "downloader.py"
])

# method two

# # 使用 shell=True 來執行複雜的指令
# subprocess.run("pyinstaller --onefile --windowed --icon=music.ico main.py", shell=True)

if os.path.exists("dist/downloader.exe") :
    if os.path.exists("downloader.exe") :
        os.remove("downloader.exe")
    shutil.move("dist/downloader.exe", "downloader.exe")
if os.path.exists("build") :        # 回收資料夾
    shutil.rmtree("build")
if os.path.exists("dist") :        # 回收資料夾
    shutil.rmtree("dist")
if os.path.exists("downloader.spec") :        # 回收資料夾
    os.remove("downloader.spec")
