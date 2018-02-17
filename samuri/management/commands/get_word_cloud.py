from wordcloud import WordCloud
from django.core.management.base import CommandError, BaseCommand
from django.db import DatabaseError
from samuri.functions import DatabaseManager as Dbm


class Command(BaseCommand):
    help = 'Generate Keyword Image for all words'

    def handle(self, *args, **options):
            all_news = Dbm().get_news_content()
            for news in all_news:
                try:
                    u_id = news.id
                    keywords = news.keywords
                    wc = WordCloud(background_color="white", max_words=100)
                    wc.generate(keywords)
                    filename = "./samuri/static/images/" + str(u_id) + ".png"
                    wc.to_file(filename)
                    self.stdout.write("Sucessfully Saved at " + filename)
                except (DatabaseError, CommandError) as err:
                    self.stdout.write(self.style.ERROR('Error in execution: "%s"' % str(err)))
