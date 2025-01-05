import config
import openai 
from news_crawler import get_news_urls, url_crawling
from prompt_template import prompt, sentiment_prompt
from datetime import datetime
import pandas as pd


OPEN_API_KEY = config.OPEN_API_KEY
openai.api_key = OPEN_API_KEY
model = "gpt-4o-mini"

def chatgpt_generate(query):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": query}
    ]

    response = openai.ChatCompletion.create(model=model, messages=messages)
    answer = response.choices[0].message.content
    return answer

#뉴스 본문을 분석하여 요약 및 감정 분석 결과를 생성
def analyze_articles(texts, titles):
    analysis_results = []

    for i, (text, title) in enumerate(zip(texts, titles)):
        print(f"\n[{i+1}] {title}")
        try:
            # 뉴스 요약 생성
            query = prompt+text
            summary = chatgpt_generate(query)
            # 감정 분석
            sentiment_query = sentiment_prompt+ summary
            sentiment = chatgpt_generate(sentiment_query)
            print("결과 저장 중...")
            # 결과 저장
            result = {
                "title": title,
                "summary": summary,
                "sentiment": sentiment
            }
            print("결과 추가 중...")
            analysis_results.append(result)
            print(f"요약: {summary}\n감정 분석: {sentiment}")

        except Exception as e:
            print(f"뉴스 분석 실패: {e}")
            continue

    return analysis_results

#분석 결과를 CSV 파일로 저장
def save_results_to_csv(results, filename):
    df = pd.DataFrame(results)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"\n분석 결과가 CSV 파일로 저장되었습니다: {filename}")


def main():
    # 분석할 기업 리스트와 검색 기간 설정
    companys = ["Apple", "Microsoft", "Google", "Amazon"]
    days = 11  # 최근 11일 뉴스 수집

    print("\n1. 뉴스 URL 수집 중...")
    articles_df = get_news_urls(companys, days=days)

    if not articles_df.empty:
        print("\n2. 뉴스 본문 추출 중...")
        texts, titles = url_crawling(articles_df)

        if texts and titles:
            print("\n3. 뉴스 분석 중...")
            analysis_results = analyze_articles(texts, titles)

            # 파일명 생성
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            csv_filename = f"news_analysis_{current_time}.csv"

            # 결과 저장
            save_results_to_csv(analysis_results, csv_filename)

            print(f"\n총 {len(analysis_results)} 개의 뉴스가 성공적으로 분석되었습니다.")
        else:
            print("\n유효한 뉴스 본문이 없습니다.")
    else:
        print("\n뉴스 URL 수집에 실패했습니다.")


if __name__ == "__main__":
    main()



