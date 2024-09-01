import os

# 取得目前的 PATH 環境變數
current_path = os.environ.get('PATH')
print(f'Current PATH: {current_path}')

# 新增一個新的目錄到 PATH
new_directory = os.path.dirname(os.path.abspath(__file__)) + '\\ffmpeg\\bin'
os.environ['PATH'] = f'{new_directory};{current_path}'

# 確認 PATH 環境變數已更新
updated_path = os.environ.get('PATH')
print(f'Updated PATH: {updated_path}')
