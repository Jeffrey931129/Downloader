import openai

# 輸入你的 OpenAI API 密鑰
openai.api_key = ''

def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # 可以使用 gpt-3.5-turbo 或 gpt-4
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()

# 與 ChatGPT 聊天
user_input = "你好，ChatGPT!"
response = chat_with_gpt(user_input)
print(response)
