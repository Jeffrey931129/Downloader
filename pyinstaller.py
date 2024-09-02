import subprocess
import os
import shutil

file_name = "downloader_v2"

# 使用列表格式來傳遞參數
subprocess.run([
    "pyinstaller",
    "--onefile",
    "--windowed",
    "--icon=music.ico",
    f"{file_name}.py"
])

# method two

# # 使用 shell=True 來執行複雜的指令
# subprocess.run("pyinstaller --onefile --windowed --icon=music.ico main.py", shell=True)

if os.path.exists(f"dist/{file_name}.exe") :
    if os.path.exists(f"{file_name}.exe") :
        os.remove(f"{file_name}.exe")
    shutil.move(f"dist/{file_name}.exe", f"{file_name}.exe")
if os.path.exists("build") :        # 回收資料夾
    shutil.rmtree("build")
if os.path.exists("dist") :        # 回收資料夾
    shutil.rmtree("dist")
if os.path.exists(f"{file_name}.spec") :        # 回收資料夾
    os.remove(f"{file_name}.spec")
