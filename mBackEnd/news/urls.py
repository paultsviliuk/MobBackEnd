from django.conf.urls import url

from . import views


urlpatterns= [
    url(r'^getAllNews/$',views.getAllNews,name='getAllNews'),
    url(r'^getLastNews/$',views.getLastNews,name='getLastNews'),
]