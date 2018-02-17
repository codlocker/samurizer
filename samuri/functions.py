from newspaper import Article
from datetime import date, timedelta
from django.utils import timezone
from samuri.models import *
from django.db import DatabaseError
import requests
import json


class NewsFeed:

    def __init__(self):
        self.API_KEY = "8526eb5151d1442cb4115f8e78cc1cb0"
        self.url = "https://newsapi.org/v2/"
        self.response = None

    def get_news_feed(self, country, from_date, content_type="everything"):
        if from_date is None:
            new_date = date.today() - timedelta(days=2)
            from_date = new_date.strftime("yyyy-mm-dd")
        complete_url = self.url + content_type + "?" + "from=" + from_date + "&sortBy=popularity&" + "country=" + country + "&apiKey=" + self.API_KEY
        self.response = requests.get(complete_url)
        return self.response.json()

    def get_complete_news(self):
        response_data = self.get_news_feed('us', None, "top-headlines")
        text_analytics = TextAnalytics()
        if response_data["status"] == "ok":
            count_news = int(response_data["totalResults"])
            for itr in range(0, count_news):
                try:
                    article_name = Article(response_data["articles"][itr]["url"], language="en")
                    article_name.download()
                    article_name.parse()
                    response_data["articles"][itr]["description"] = article_name.text
                    response_data["articles"][itr]["score"] = text_analytics.perform_sentimental_analysis(response_data["articles"][itr]["description"])
                    keywords = text_analytics.get_keywords(response_data["articles"][itr]["description"], "en")
                    response_data["articles"][itr]["keywords"] = ''
                    for key in keywords:
                        response_data["articles"][itr]["keywords"] += (key + ",")
                except Exception as ex:
                    response_data["articles"][itr] = None
            return response_data["articles"]
        else:
            return None

    def store_news_to_db(self):
        all_articles = self.get_complete_news()
        count = 0
        for news in all_articles:
            if news is None:
                continue
            print(news["score"])
            try:
                check_exists = NewsContent.objects.filter(headline=news["title"]).exists()
                if not check_exists:
                    if news["urlToImage"]:
                        add_news = NewsContent(headline=news["title"], content=news["description"],
                                               source_link=news["url"],
                                               language='EN', date_added=timezone.now(), post_date=news["publishedAt"],
                                               image_link=news["urlToImage"], sentiment_score=news["score"], keywords=news["keywords"])
                        add_news.save()
                    else:
                        add_news = NewsContent(headline=news["title"], content=news["description"],
                                               source_link=news["url"], language='EN', date_added=timezone.now(),
                                               post_date=news["publishedAt"], sentiment_score=news["score"], keywords=news["keywords"])
                        add_news.save()
                    count += 1
            except DatabaseError as de:
                print(str(de))
        return count, len(all_articles)


class DatabaseManager:

    def __init__(self):
        pass

    def get_news_content(self):
        all_data = NewsContent.objects.all()
        return all_data


class TextAnalytics:
    def __init__(self):
        self.api_key = "65ed14d0e3604c16875f757e9bf77924"
        self.api_url = "https://southeastasia.api.cognitive.microsoft.com/text/analytics/v2.0/"
        self.headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.api_key,
        }

    def perform_sentimental_analysis(self, text="I am Khan and I am not a terrorist", lang="en"):
        url = self.api_url + 'sentiment'
        print(len(text))
        if len(text) > 5000:
            text = text[0:5000]
        body = {
            "documents": [
                {
                    "id": "1",
                    "text": text,
                    "language": lang
                }
            ]
        }
        try:
            response = requests.post(url, headers=self.headers, data=json.dumps(body))
            data = response.json()
            if 'documents' in data and len(data["documents"]) > 0:
                score = data['documents'][0]['score']
                return float(score)
            else:
                return None
        except Exception as e:
            print(str(e))

    def get_keywords(self, text="I am Khan and I am not a terrorist", lang="en"):
        url = self.api_url + 'keyPhrases'
        print(len(text))
        if len(text) > 5000:
            text = text[0:5000]
        body = {
            "documents": [
                {
                    "id": "1",
                    "text": text,
                    "language": lang
                }
            ]
        }
        try:
            response = requests.post(url, headers=self.headers, data=json.dumps(body))
            data = response.json()
            if 'documents' in data and len(data['documents']) > 0:
                return data['documents'][0]['keyPhrases']
        except Exception as e:
            print(str(e))
