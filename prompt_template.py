prompt = """
아래 뉴스 텍스트를 참고하여 세 가지 task를 수행하시오. 결과는 반드시 **순수 JSON 형식**으로 반환하십시오.
**어떠한 추가적인 텍스트, 코드 블록(````json`)도 포함하지 마십시오.**

Task #1: 텍스트를 참고해서 다음과 같은 카테고리로 분류하시오. 아래 카테고리에 해당하지 않으면, 빈 리스트를 반환하시오.

카테고리: 정책/금융, 채권/외환, IB/기업, 증권, 국제뉴스, 해외주식, 부동산

Task #2: 뉴스 내용을 최대 3문장으로 요약하시오.

Task #3: 뉴스에서 금융 이벤트 예시를 참고하여 내용과 관련된 이벤트를 생성하시오.
예시에 있는 이벤트가 아닌 뉴스와 관련된 이벤트 문구를 반드시 새로 생성하시오.

금융 이벤트 예시: "신제품 출시", "기업 인수합병", "리콜", "배임횡령", "오너 리스크", "자연재해", "제품 불량" 등

출력 예시:
{
    "문서 카테고리": <카테고리>,
    "요약": <요약 문장>,
    "주요 이벤트": [<이벤트1>, <이벤트2>, ...]
}

뉴스:
"""

sentiment_prompt = """
다음 뉴스 요약에 기반하여 뉴스의 전반적인 감정을 분석해주세요. 감정은 긍정적(Positive), 중립적(Neutral), 부정적(Negative) 중 하나로 선택하고, 선택한 이유를 간단히 설명해주세요.
결과는 반드시 **순수 JSON 형식**으로 반환하십시오.
**어떠한 추가적인 텍스트, 코드 블록(````json`)도 포함하지 마십시오.**

결과 형식:
- 감정: (Positive/Neutral/Negative)
- 이유: (간단한 설명)

뉴스 요약:
"""