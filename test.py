import requests

# 發送請求並保存 Cookie
session = requests.Session()
response = session.get('https://www.youtube.com')

# 將 Cookie 保存到 cookies.txt
with open('test.txt', 'w') as file:
    for cookie in session.cookies:
        file.write(f"{cookie.domain}\tTRUE\t{cookie.path}\t{'TRUE' if cookie.secure else 'FALSE'}\t{cookie.expires}\t{cookie.name}\t{cookie.value}\n")
