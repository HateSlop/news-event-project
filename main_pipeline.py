from news_crawler import NewsCrawler
from news_classifier import NewsClassifier
from db_manager import DBManager
from visualization import NewsVisualization
import streamlit as st
import time

def run_pipeline():
    """전체 뉴스 처리 파이프라인을 실행합니다."""
    try:
        print("=== 뉴스 파이프라인 시작 ===")
        
        # 1. 뉴스 크롤러 초기화 및 데이터 수집
        print("\n1. 뉴스 수집 시작...")
        crawler = NewsCrawler()
        keywords = ["Apple", "Tesla", "Microsoft", "Google", "Amazon", "Meta"]
        articles_df = crawler.get_news_urls(keywords, days=14)
        
        if articles_df.empty:
            print("수집된 뉴스가 없습니다.")
            return
            
        # 2. 뉴스 본문 추출
        print("\n2. 뉴스 본문 추출 중...")
        texts, titles = crawler.extract_article_content(articles_df)
        
        # 3. 뉴스 분류 및 요약
        print("\n3. 뉴스 분석 중...")
        classifier = NewsClassifier()
        results = classifier.process_news_batch(articles_df)
        
        if not results:
            print("분석된 결과가 없습니다.")
            return
            
        # 4. MongoDB에 결과 저장
        print("\n4. 분석 결과 저장 중...")
        db_manager = DBManager()
        db_manager.save_news_results(results)
        
        print("\n=== 파이프라인 실행 완료 ===")
        
    except Exception as e:
        print(f"파이프라인 실행 중 오류 발생: {e}")

def main():
    """메인 함수"""
    print("뉴스 이벤트 분석 시스템을 시작합니다...")
    run_pipeline()

if __name__ == "__main__":
    main()
