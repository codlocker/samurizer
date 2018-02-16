import requests
from newspaper import Article
from datetime import date, timedelta
from django.utils import timezone
from samuri.models import *
from django.db import DatabaseError


class NewsFeed:

    def __init__(self):
        self.API_KEY = "8526eb5151d1442cb4115f8e78cc1cb0"
        self.url = "https://newsapi.org/v2/"
        self.response = None

    def get_news_feed(self, country, from_date, content_type="everything"):
        if from_date is None:
            new_date = date.today() - timedelta(days=2)
            from_date = new_date.strftime("yyy-mm-dd")
        complete_url = self.url + content_type + "?" + "from=" + from_date + "&sortBy=popularity&" + "country=" + country + "&apiKey=" + self.API_KEY
        self.response = requests.get(complete_url)
        return self.response.json()

    def get_complete_news(self):
        response_data = self.get_news_feed('us', None, "top-headlines")
        if response_data["status"] == "ok":
            count_news = int(response_data["totalResults"])
            for itr in range(0, count_news):
                try:
                    article_name = Article(response_data["articles"][itr]["url"], language="en")
                    article_name.download()
                    article_name.parse()
                    response_data["articles"][itr]["description"] = article_name.text
                except Exception as ex:
                    print(str(ex))
            return response_data["articles"]
        else:
            return None

    def store_news_to_db(self):
        all_articles = self.get_complete_news()
        count = 0
        for news in all_articles:
            try:
                check_exists = NewsContent.objects.filter(headline=news["title"]).exists()
                if not check_exists:
                    if news["urlToImage"]:
                        add_news = NewsContent(headline=news["title"], content=news["description"],
                                               source_link=news["url"],
                                               language='EN', date_added=timezone.now(), post_date=news["publishedAt"],
                                               image_link=news["urlToImage"])
                        add_news.save()
                    else:
                        add_news = NewsContent(headline=news["title"], content=news["description"],
                                               source_link=news["url"], language='EN', date_added=timezone.now(),
                                               post_date=news["publishedAt"])
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
