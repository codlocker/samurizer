from django.db import models
LANGUAGE_LIST = (
    ('en', 'English'),
    ('hi', 'Hindi'),
    ('ta', 'Tamil'),
    ('ur', 'Urdu')
)


class NewsContent(models.Model):
    headline = models.TextField(default='No heading given')
    content = models.TextField(default='News Content')
    summarized_data = models.TextField(default='Summary')
    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_LIST,
        default='EN'
    )
    date_added = models.DateTimeField('The time details')
    post_date = models.DateTimeField('Post Addition Date')
    source_link = models.TextField(default='None')
    image_link = models.URLField(default='/images/no-image.png', max_length=1000)
    sentiment_score = models.FloatField(default=0.0)
    keywords = models.TextField(default='None')
