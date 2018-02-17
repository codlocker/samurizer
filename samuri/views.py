from django.shortcuts import render
from samuri.functions import DatabaseManager as DbM
from django.http import JsonResponse
# Create your views here.
db_manager = DbM()


def index(request):
    all_data = db_manager.get_news_content()
    return render(request, 'index.html', context={"all_articles": all_data})


def parse(request):
    response = {}
    if request.method == "POST":
        qid = request.POST.get("question_id")
        language = request.POST.get("language")
        response = db_manager.get_translated_news(qid, language)
        if response is not None:
            response["id"] = 200
        else:
            response["id"] = 300
    else:
        response["id"] = 500
    return JsonResponse(response)
