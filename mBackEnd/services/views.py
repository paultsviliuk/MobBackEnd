from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, Http404
from .models import Services, PromoCodes,ServicesCosts
from account_managment.models import UserTokken,UserServices
from account_managment import mail
import json
import datetime

# Create your views here
all_services = Services.objects.all()
all_costs=ServicesCosts.objects.all()
promo_codes=PromoCodes.objects
tokkens=UserTokken.objects

def getAllServices(request):
    dic=[{'service_name':s.service_name,'id': s.id,'description': s.description,'price': c.price,'duration':c.duration, 'srv_image':s.image.url}
         for s in all_services for c in all_costs.filter(service=s)]
    return JsonResponse(dic,safe=False)

def activatePromoCode(request):
    if request.method=='POST':
        request_info = str(request.body, 'utf-8')
        promo_info = json.loads(request_info)

        try:
            promo_code=promo_info['promo code']
            tokken=promo_info['tokken']
        except :
            return HttpResponseBadRequest('Illegal arguments')

        try:
            tokken=tokkens.get(user_tokken=tokken)
        except :
            return HttpResponseBadRequest('Illegal tokken')

        try:
            promo_code = promo_codes.get(promo_code=promo_code)
        except :
            return HttpResponseBadRequest('Illegal promo code')

        try:
            user_service = UserServices.objects.get(service=promo_code.service, user=tokken.user)

            date = getEndTime(user_service.end_time,promo_code.duration)
            if date.year-datetime.datetime.today().year<=1 and date.month-datetime.datetime.today().date().month<=1:
                user_service = UserServices(promo_code.service.id, tokken.user.id, date)
                user_service.save()
                return HttpResponse('service has been activated')
            else: 
                return HttpResponseBadRequest('you cant use this promocode')

        except :
            date = getEndTime(datetime.datetime.today(), promo_code.duration)
            user_service=UserServices(promo_code.service.id,tokken.user.id,date)
            user_service.save()
            promo_code.delete()
            return HttpResponse('service has been activated')
    else:
        return Http404("Illegal method")

def activateService(request):
    if request.method=='POST':
        request_info = str(request.body, 'utf-8')
        request_info = json.loads(request_info)
        try:
            service_id=request_info['service id']
            tokken=request_info['tokken']
            duration=int(request_info['duration'])
        except :
            return HttpResponseBadRequest('Illegal arguments')

        try:
            tokken=tokkens.get(user_tokken=tokken)
        except :
            return HttpResponseBadRequest('Illegal tokken')

        try:
            service=all_services.get(id=service_id)
        except :
            return HttpResponseBadRequest('Illegal service id')


        try:
            user_service=UserServices.objects.get(service=service, user=tokken.user)

            date = getEndTime(user_service.end_time,duration)
            if date.year-datetime.datetime.today().year<=1 and date.month-datetime.datetime.today().date().month<=1:
                user_service = UserServices(service.id, tokken.user.id, date)
                user_service.save()
                return HttpResponse('service has been activated')
            else: 
                return HttpResponseBadRequest('you cant activate this service')

        except :
            date = getEndTime(datetime.datetime.today(), duration)
            user_service=UserServices(service.id,tokken.user.id,date)
            user_service.save()
            return HttpResponse('service has been activated')

    else:
        return Http404("Illegal method")

def checkServiceForBuying(request):
    if request.method=='POST':
        request_info = str(request.body, 'utf-8')
        request_info = json.loads(request_info)
        try:
            service_id=request_info['service id']
            tokken=request_info['tokken']
            duration=int(request_info['duration'])
        except :
            return HttpResponseBadRequest('Illegal arguments')

        try:
            tokken=tokkens.get(user_tokken=tokken)
        except :
            return HttpResponseBadRequest('Illegal tokken')

        try:
            service=all_services.get(id=service_id)
        except :
            return HttpResponseBadRequest('Illegal service id')


        try:
            user_service=UserServices.objects.get(service=service, user=tokken.user)

            date = getEndTime(user_service.end_time,duration)
            if date.year-datetime.datetime.today().year<=1 and date.month-datetime.datetime.today().date().month<=1:
                a = True
                dic = {'can buy': a}
                return JsonResponse(dic)
            else:
                a = False
                dic = {'can buy': a}
                return JsonResponse(dic)

            a = False
            dic = {'can buy': a}
            return JsonResponse(dic)

        except :
            a=True
            dic={'can buy':a}
            return JsonResponse(dic)

    else:
        return Http404("Illegal method")


def checkPromoCodeIsExist(request):
    if request.method == 'POST':
        request_info = str(request.body, 'utf-8')
        request_info = json.loads(request_info)
        try:
            service_id=request_info['service id']
            duration = int(request_info['duration'])
        except :
            return HttpResponseBadRequest('Illegal arguments')

        try:
            service=all_services.get(id=service_id)
            if promo_codes.filter(duration=duration,service=service).count()!=0:
                a = True
                dic = {'can buy': a}
                return JsonResponse(dic)
            else:
                a = False
                dic = {'can buy': a}
                return JsonResponse(dic)
        except:
           return HttpResponseBadRequest('Illegal service id')

    else:
        return Http404("Illegal method")



def getPromocode(request):
    if request.method == 'POST':
        request_info = str(request.body, 'utf-8')
        request_info = json.loads(request_info)
        try:
            service_id=request_info['service id']
            tokken = request_info['tokken']
            duration = int(request_info['duration'])
        except :
            return HttpResponseBadRequest('Illegal arguments')

        try:
            service = all_services.get(id=service_id)
        except:
            return HttpResponseBadRequest('Illegal service id')

        try:
            tokken = tokkens.get(user_tokken=tokken)
        except:
            return HttpResponseBadRequest('Illegal tokken')

        try:
            promo_code=promo_codes.filter(duration=duration,service=service)[0]
            mail.sendPromoCode(tokken.user.email,promo_code.promo_code)
            promo_code.delete()
            return HttpResponse('email has been sent')

        except:
            return HttpResponseBadRequest('Promo code is not exist')


    else:
        return Http404("Illegal method")



def getEndTime(date,duration):
    month=date.month
    year=date.year
    if month+duration>12:
        year+=1
        month+=duration-12
    else:
        month+=duration
    return datetime.date(year,month,date.day)
