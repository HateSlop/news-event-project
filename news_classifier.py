# 뉴스 요약 및 이벤트 추출 기능
# 3. 기사 요약 및 이벤트 추출

# 뉴스들에서 이벤트 추출과 요약을 실행

import config
from openai import OpenAI

OPENAI_API_KEY = config.OPENAI_API_KEY
openai_client = OpenAI(api_key=OPENAI_API_KEY)
model = "gpt-4o-mini"

def chatgpt_generate(query):
    messages = [{
        "role": "system",
        "content" : "You are a helpful assistant."},
        {
            "role": "user",
            "content": query
        }]
    response = openai_client.chat.completions.create(model=model, messages=messages)
    answer = response.choices[0].message.content
    return answer
