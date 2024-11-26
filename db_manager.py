from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
import json
import os
import config
from pymongo import MongoClient
from datetime import datetime

class DBManager:
    def __init__(self):
        # MongoDB 연결 - 로컬 MongoDB 서버
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['newsdb']
        self.collection = self.db['news_events']
        
    def save_news_results(self, results):
        """뉴스 분석 결과를 MongoDB에 저장합니다."""
        try:
            for result in results:
                # 저장할 문서 생성
                doc = {
                    'title': result.get('제목', ''),
                    'url': result.get('URL', ''),
                    'domain': result.get('도메인', ''),
                    'published_date': result.get('게시일', ''),
                    'category': result.get('문서 카테고리', []),
                    'summary': result.get('요약', ''),
                    'events': result.get('주요 이벤트', []),
                    'sentiment': result.get('감성분석', {}),
                    'analysis_date': result.get('분석_날짜', ''),
                    'created_at': datetime.now()
                }
                
                # 빈 리스트나 빈 딕셔너리 필터링
                doc = {k: v for k, v in doc.items() if v != [] and v != {}}
                
                # MongoDB에 저장
                self.collection.insert_one(doc)
                
            print(f"{len(results)}개의 뉴스 분석 결과가 MongoDB에 저장되었습니다.")
            
        except Exception as e:
            print(f"MongoDB 저장 중 오류 발생: {e}")
            
    def get_recent_news(self, limit=10):
        """최근 저장된 뉴스를 조회합니다."""
        try:
            cursor = self.collection.find().sort('created_at', -1).limit(limit)
            return list(cursor)
        except Exception as e:
            print(f"뉴스 조회 중 오류 발생: {e}")
            return []
            
    def get_news_by_category(self, category):
        """카테고리별 뉴스를 조회합니다."""
        try:
            cursor = self.collection.find({'category': category})
            return list(cursor)
        except Exception as e:
            print(f"카테고리 조회 중 오류 발생: {e}")
            return []

def main():
    try:
        # 뉴스 크롤러 초기화 및 데이터 수집
        from news_crawler import NewsCrawler
        crawler = NewsCrawler()
        keywords = ["Apple"] # "Tesla", "Microsoft", "Google", "Amazon", "Meta"]
        articles_df = crawler.get_news_urls(keywords)
        
        if not articles_df.empty:
            # 뉴스 본문 추출
            texts, titles = crawler.extract_article_content(articles_df)
            
            # 뉴스 분류 및 요약
            from news_classifier import NewsClassifier
            classifier = NewsClassifier()
            results = classifier.process_news_batch(articles_df)
            
            # MongoDB에 저장
            db_manager = DBManager()
            db_manager.save_news_results(results)
            
            # 저장된 결과 확인
            recent_news = db_manager.get_recent_news(5)
            print("\n=== 최근 저장된 뉴스 ===")
            for news in recent_news:
                print(news)

                
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    main()