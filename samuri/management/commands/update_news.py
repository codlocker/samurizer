from django.core.management.base import CommandError, BaseCommand
from django.db import DatabaseError
from samuri.functions import NewsFeed


class Command(BaseCommand):
    help = 'Just do it'

    def handle(self, *args, **options):
        try:
            news = NewsFeed()
            pr, tot = news.store_news_to_db()
            text = "{} / {} data was added to the database".format(pr, tot)
            self.stdout.write(self.style.WARNING(text))
        except (DatabaseError, CommandError) as err:
            self.stdout.write(self.style.ERROR('Error in execution: "%s"' % str(err)))
