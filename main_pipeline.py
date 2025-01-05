import json
from news_crawler import url_crawling, get_news_urls
from news_classifier import analyze_articles
from db_manager import save_news_results

# 모든 회사 이름을 저장하는 목록
companies = ["Apple", "Microsoft", "Google", "Amazon"]

try:
    for company in companies:  # 모든 회사에 대해 반복
        print(f"\n{company}에 대한 뉴스 처리 시작")

        # 뉴스 URL 가져오기
        articles_df = get_news_urls([company], days=10)  # 여기서 회사 이름을 리스트로 전달

        if not articles_df.empty:
            print(f"\n{company}의 뉴스 본문 추출 중...")
            texts, titles = url_crawling(articles_df)

            # 데이터 프레임에서 날짜 가져오기
            dates = articles_df['date'].tolist()

        if texts and titles:
            print(f"\n{company}의 뉴스 분석 중...")
            analysis_results = analyze_articles(texts, titles)

            # 결과 저장
            for i in range(len(titles)):
                data_dict = {
                    "title": titles[i],
                    "text": texts[i],
                    "summary": analysis_results[i]["summary"],  # 해당 결과의 요약 추출
                    "sentiment": analysis_results[i]["sentiment"],  # 해당 결과의 감정 분석 추출
                    "date": dates[i]  
                }
                raw_data = json.dumps(data_dict, default=str)
                save_news_results(raw_data, company=company)  # 각 회사별로 데이터 저장

except Exception as e:
    print(f"오류 발생: {e}")
