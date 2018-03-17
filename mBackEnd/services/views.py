from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, Http404
from .models import Services, PromoCodes,ServicesCosts
from account_managment.models import UserTokken,UserServices,UserActivatedPromoCodes,User
from account_managment import mail
import json
import datetime

# Create your views here
all_services = Services.objects
all_costs=ServicesCosts.objects
promo_codes=PromoCodes.objects
tokkens=UserTokken.objects


def getAllServices(request):
    dic=[{'service_name':s.service_name,'id': s.id,'description': s.description,'price': c.price,'duration':c.duration, 'srv_image':s.image.url}
         for s in all_services.filter(activated_type='активная').order_by('id') for c in all_costs.filter(service=s)]
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
            user = User.objects.get(id=tokken.user.id)
            if user.activated_promo_codes == None:
                user.activated_promo_codes = ''

            if date.year - datetime.datetime.today().year < 1:
                user_service = UserServices(user_service.id,promo_code.service.id, tokken.user.id, date)
                user_service.save()
                user_activated_promo_code = UserActivatedPromoCodes(user_service.id, promo_code.promo_code,promo_code.duration,promo_code.cause_of_reservation)
                user_activated_promo_code.save()
                user.activated_promo_codes += user_service.service.service_name + "Promo code: " + promo_code.promo_code + " Duration: " + \
                                              str(date) + "\n "
                user.save()
                promo_code.delete()
                return HttpResponse('service has been activated')
            if date.year - datetime.datetime.today().year == 1 and date.month - datetime.datetime.today().date().month <= 1:
                user_service = UserServices(user_service.id,promo_code.service.id, tokken.user.id, date)
                user_service.save()
                user_activated_promo_code = UserActivatedPromoCodes(user_service.id, promo_code.promo_code,promo_code.duration,promo_code.cause_of_reservation)
                user_activated_promo_code.save()
                user.activated_promo_codes += user_service.service.service_name + "Promo code: " + promo_code.promo_code + " Duration: " + \
                                              str(date) + "\n "
                user.save()
                promo_code.delete()
                return HttpResponse('service has been activated')
            else:
                return HttpResponseBadRequest('you cant use this promocode now')

        except :
            date = getEndTime(datetime.datetime.today(), promo_code.duration)
            user_services = UserServices.objects.all()
            user = User.objects.get(id=tokken.user.id)
            if user.activated_promo_codes == None:
                user.activated_promo_codes = ''

            if user_services.count() > 0:
                user_service = UserServices(user_services[user_services.count()-1].id + 1, promo_code.service.id, tokken.user.id, date)
                user_service.save()
                user_activated_promo_code=UserActivatedPromoCodes(user_service.id, promo_code.promo_code,promo_code.duration,promo_code.cause_of_reservation)
                user_activated_promo_code.save()
                user.activated_services += "Service: " + user_service.service.service_name + "\n"
                user.activated_promo_codes += user_service.service.service_name + "Promo code: " + promo_code.promo_code + " Duration: " + \
                                              str(date) + "\n "
                user.save()
                promo_code.delete()
                return HttpResponse('service has been activated')
            else:
                user_service = UserServices(0, promo_code.service.id, tokken.user.id, date)
                user_service.save()
                user_activated_promo_code = UserActivatedPromoCodes(user_service.id, promo_code.promo_code,promo_code.duration,promo_code.cause_of_reservation)
                user_activated_promo_code.save()
                user.activated_services += "Service: " + user_service.service.service_name + "\n"
                user.activated_promo_codes += user_service.service.service_name + "Promo code: " + promo_code.promo_code + " Duration: " + \
                                              str(date) + "\n "
                user.save()
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
            promo_codes = PromoCodes.objects.filter(cause_of_reservation=None,duration=duration)
            user=User.objects.get(id=tokken.user.id)
            if user.activated_promo_codes==None and user.activated_services==None:
                user.activated_promo_codes=''
                user.activated_services=''

            if promo_codes.count()>0 and str(service.activated_type)!='не активная':
                date = getEndTime(user_service.end_time,duration)
                if date.year-datetime.datetime.today().year<1:
                    user_service = UserServices(user_service.id,service.id, tokken.user.id, date)
                    user_activated_promo_code = UserActivatedPromoCodes(user_service.id, promo_codes[0].promo_code,promo_codes[0].duration,promo_codes[0].cause_of_reservation)
                    user_activated_promo_code.save()
                    user.activated_promo_codes += user_service.service.service_name + "Promo code: " + promo_codes[0].promo_code + " Duration: " + \
                                                  str(date) + "\n "
                    user.save()
                    promo_codes[0].delete()
                    user_service.save()
                    return HttpResponse('service has been activated')
                if date.year-datetime.datetime.today().year==1 and date.month-datetime.datetime.today().date().month<=1:
                    user_service = UserServices(user_service.id,service.id, tokken.user.id, date)
                    user_activated_promo_code = UserActivatedPromoCodes(user_service.id, promo_codes[0].promo_code,promo_codes[0].duration,promo_codes[0].cause_of_reservation)
                    user_activated_promo_code.save()
                    user.activated_promo_codes += user_service.service.service_name + "Promo code: " + promo_codes[0].promo_code + " Duration: " + \
                                                  str(date) + "\n "
                    user.save()
                    promo_codes[0].delete()
                    user_service.save()
                    return HttpResponse('service has been activated')
                else:
                    return HttpResponseBadRequest('you cant activate this service')
            else:
                return HttpResponseBadRequest('you cant activate this service, because in database there arent any promocodes')

        except :
            date = getEndTime(datetime.datetime.today(), duration)
            user = User.objects.get(id=tokken.user.id)
            if user.activated_promo_codes==None and user.activated_services==None:
                user.activated_promo_codes=''
                user.activated_services=''


            promo_codes = PromoCodes.objects.filter(cause_of_reservation=None,duration=duration)

            if promo_codes.count() > 0 and str(service.activated_type)!='не активная':
                user_services=UserServices.objects.all()
                if user_services.count()>0:
                    user_service=UserServices(user_services[user_services.count()-1].id + 1,service.id, tokken.user.id,date)
                    user_activated_promo_code = UserActivatedPromoCodes(user_service.id, promo_codes[0].promo_code,promo_codes[0].duration,promo_codes[0].cause_of_reservation)
                    user_activated_promo_code.save()
                    user.activated_services += "Service: " + user_service.service.service_name + "\n "
                    user.activated_promo_codes += user_service.service.service_name + "Promo code: "+promo_codes[0].promo_code+" Duration: "+str(date)+"\n "
                    user.save()
                    promo_codes[0].delete()
                    user_service.save()
                    return HttpResponse('service has been activated')
                else:
                    user_service = UserServices(0, service.id, service, tokken.user.id, date)
                    user_activated_promo_code = UserActivatedPromoCodes(user_service.id, promo_codes[0].promo_code,promo_codes[0].duration,promo_codes[0].cause_of_reservation)
                    user_activated_promo_code.save()
                    user.activated_services += "Service: " + user_service.service.service_name + "\n "
                    user.activated_promo_codes += user_service.service.service_name + "Promo code: " + promo_codes[0].promo_code + " Duration: " + \
                                                  str(date) + "\n "
                    user.save()
                    promo_codes[0].delete()
                    user_service.save()
                    return HttpResponse('service has been activated')
            else:
                return HttpResponseBadRequest(
                    'you cant activate this service, because in database there arent any promocodes')

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

        promo_codes = PromoCodes.objects.filter(cause_of_reservation=None,duration=duration)

        if str(service.activated_type)=='не активная' or promo_codes.count()==0 :
            a = False
            dic = {'can buy': a}
            return JsonResponse(dic)

        try:
            user_service=UserServices.objects.get(service=service, user=tokken.user)

            date = getEndTime(user_service.end_time,duration)
            if date.year-datetime.datetime.today().year<1:
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
    elif month+duration>24:
        year+=2
        month+=duration-24
    elif month+duration>36:
        year+=3
        month+=duration-36
    elif month+duration>48:
        year+=4
        month+=duration-48
    elif month+duration>60:
        year+=5
        month+=duration-60
    else:
        month+=duration
    try:
        return datetime.date(year,month,date.day)
    except:
        if month==2:
            return datetime.date(year,month,date.day-3)
        else:
            return datetime.date(year, month, date.day - 1)
