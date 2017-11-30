from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, Http404
from .models import News

# Create your views here.
news=News.objects

def getAllNews(request):
    nw=news.all()
    dic = [{'news_name':n.news_name, 'id':n.id, 'news_image':n.news_image.url, 'news_information':n.news_information}
            for n in nw]
    return JsonResponse(dic, safe=False)

def getLastNews(request):
    nw = news.all()
    count=nw.count()
    if count >= 10:
        dic = [{'news_name':n.news_name, 'id':n.id,'news_image':n.news_image.url, 'news_information':n.news_information}
               for n in nw[count-10:]]
    else:
        dic = [{'news_name': n.news_name, 'id': n.id,'news_image':n.news_image.url, 'news_information':n.news_information}
                for n in nw]
    return JsonResponse(dic, safe=False)
