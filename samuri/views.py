from django.shortcuts import render
from samuri.functions import DatabaseManager as DbM
# Create your views here.


def index(request):
    db_manager = DbM()
    all_data = db_manager.get_news_content()
    return render(request, 'index.html', context={"all_articles": all_data})
