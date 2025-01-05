sentiment_prompt = """
다음 뉴스 요약에 기반하여 뉴스의 전반적인 감정을 분석해주세요. 감정은 긍정적(Positive), 중립적(Neutral), 부정적(Negative) 중 하나로 선택하고, 선택한 이유를 간단히 설명해주세요.

뉴스 요약:
"{summary}"

결과 형식:
- 감정: (Positive/Neutral/Negative)
- 이유: (간단한 설명)
"""