from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^getAllServices/$',views.getAllServices,name='getAllServices'),
    url(r'^activatePromoCode/$',views.activatePromoCode,name='activatePromoCode'),
    url(r'^activateService/$',views.activateService,name='acticateService'),
    url(r'^checkServiceForBuying/$',views.checkServiceForBuying,name='checkServiceForBuying'),
    url(r'checkPromoCodeIsExist/$',views.checkPromoCodeIsExist,name='checkPromoCodeIsExist'),
    url(r'getPromocode/$',views.getPromocode,name='getPromocode')
]