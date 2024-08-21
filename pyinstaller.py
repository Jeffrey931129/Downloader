import subprocess
import os
import shutil

# 使用列表格式來傳遞參數
subprocess.run([
    "pyinstaller",
    "--onefile",
    "--windowed",
    "--icon=music.ico",
    "main.py"
])

# method two

# # 使用 shell=True 來執行複雜的指令
# subprocess.run("pyinstaller --onefile --windowed --icon=music.ico main.py", shell=True)

if os.path.exists("dist/main.exe") :
    os.remove("main.exe")
    shutil.move("dist/main.exe", "main.exe")
if os.path.exists("build") :        # 回收資料夾
    shutil.rmtree("build")
if os.path.exists("dist") :        # 回收資料夾
    shutil.rmtree("dist")
if os.path.exists("main.spec") :        # 回收資料夾
    os.remove("main.spec")
