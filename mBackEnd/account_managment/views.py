from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, Http404
from .models import User, UserTokken,UserServices
from . import mail, generationCodes
import json
import datetime
import requests


# Create your views here.
users=User.objects
tokkens = UserTokken.objects
user_services=UserServices.objects

def getUsers(request):
    return HttpResponse(users)

def getUserInfo(request,tokken):
    try:
        tokken=tokkens.get(user_tokken=tokken)
        user_info={'name':tokken.user.name,
               'surname':tokken.user.surname,
               'email':tokken.user.email,
                'telephone':tokken.user.telephone
               }
        json_response=JsonResponse(user_info)
        return json_response

    except :
        return HttpResponseBadRequest("Illegal tokken")


def addUser(request):
    if request.method=='POST':
        request_info=str(request.body,'utf-8')
        user_info=json.loads(request_info)

        try:
            name=user_info['name']
            surname=user_info['surname']
            email=user_info['email']
            password=user_info['password']
            telephone=int(user_info['telephone'])

        except :
            return HttpResponseBadRequest("Illegal arguments")


        if users.filter(email=email).count()!=0:
            return HttpResponseBadRequest("this email is in use")
        if users.filter(telephone=telephone).count()!=0:
            return HttpResponseBadRequest("this phone is in use")

        try:
            new_user=User(users.all().count()+1,name,surname,email,password,telephone)
            tokken=generationCodes.makeTokken()
            new_user.save()
            new_user_tokken=UserTokken(tokkens.all().count()+1,tokken,new_user.id)
            new_user_tokken.save()
            dic={'tokken':tokken}
            json_response=JsonResponse(dic)
            return json_response

        except :
            return HttpResponseBadRequest("Illegal arguments")


    else:
        return Http404("Illegal method")


def authorizeUser(request):
    if request.method=='POST':
        request_info = str(request.body, 'utf-8')
        user_info = json.loads(request_info)
        try:
            telephone=user_info['telephone']
            password=user_info['password']
            email=user_info['email']
            if telephone!='':
                user=users.get(telephone=telephone,password=password)
                tokken=tokkens.get(user=user)
                dic = {'tokken': tokken.user_tokken}
                json_response = JsonResponse(dic)
                return json_response
            if email!='':
                user = users.get(email=email, password=password)
                tokken = tokkens.get(user=user)
                dic = {'tokken': tokken.user_tokken}
                json_response = JsonResponse(dic)
                return json_response
            return HttpResponseBadRequest("Illegal arguments")
        except BaseException:
            return HttpResponseBadRequest("Illegal arguments")

    else:
        return Http404("Illegal method")

def getPassword(request):
    if request.method=='POST':
        request_info = str(request.body, 'utf-8')
        user_info = json.loads(request_info)
        try:
            email=user_info['email']
            telephone=user_info['telephone']
        except :
            return HttpResponseBadRequest("Illegal argumets")

        if email!='':
            if users.filter(email=email).count()!=0:
                user=users.get(email=email)
                mail.sendPassword(email,user.password)
                return HttpResponse("Message has been sent")
            else:
                return HttpResponseBadRequest("An account with this email address does not exist")

        if telephone!='':
            if users.filter(telephone=telephone).count()!=0:
                user=users.get(telephone=telephone)
                mail.sendPassword(email,user.password)
                return HttpResponse("Message has been sent")
            else:
                return HttpResponseBadRequest("An account with this telephone address does not exist")

    else:
        return Http404("Illegal method")

def changePassword(request,tokken):
    if request.method=='POST':
        request_info = str(request.body, 'utf-8')
        user_info = json.loads(request_info)
        try:
            new_password=user_info['password']
        except :
            return HttpResponseBadRequest("Illegal arguments")

        try:
            tokken = tokkens.get(user_tokken=tokken)
            tokken.user.password=new_password
            tokken.user.save()
            return HttpResponse("Password has changed")
        except :
            return HttpResponseBadRequest("Illegal tokken")
    else:
        return Http404("Illegal method")

def changeTelephone(request, tokken):
    if request.method=='POST':
        request_info = str(request.body, 'utf-8')
        user_info = json.loads(request_info)
        try:
            new_telephone = user_info['telephone']
        except:
            return HttpResponseBadRequest("Illegal arguments")

        try:
            tokken = tokkens.get(user_tokken=tokken)
            tokken.user.telephone=new_telephone
            tokken.user.save()
            return HttpResponse("Telephone has changed")
        except:
            return HttpResponseBadRequest("Illegal tokken")
    else:
        return Http404("Illegal method")


def checkUserService(request):
    if request.method=='POST':
        request_info = str(request.body, 'utf-8')
        request_info = json.loads(request_info)
        try:
            service_id=request_info['service id']
            tokken=request_info['tokken']
        except :
            return HttpResponseBadRequest('Illegal arguments')

        try:
            tokken = tokkens.get(user_tokken=tokken)
        except :
            return HttpResponseBadRequest('Illegal tokken')

        try:
            a=False
            service_id=int(service_id)
            for service in user_services.filter(user=tokken.user):
                if service.service.id==service_id:
                    if service.end_time>datetime.datetime.today().date():
                        a=True
                        break
                    else:
                        service.delete()
                        break

            dic={'available':a}
            return JsonResponse(dic)
        except :
            return HttpResponseBadRequest('Illegal service id')
    else:
        return Http404("Illegal method")

def getAllUserServices(request,tokken):
    try:
        tokken = tokkens.get(user_tokken=tokken)
    except BaseException:
        return HttpResponseBadRequest('Illegal tokken')

    all_services=user_services.filter(user=tokken.user)

    for service in all_services:
        if service.end_time < datetime.datetime.today().date():
            service.delete()

    all_services = user_services.filter(user=tokken.user)
    dic = [{'service_name': s.service.service_name, 'id': s.service.id, 'description': s.service.description,
            'srv_image': s.service.image.url, 'end date': s.end_time}
           for s in all_services]

    return JsonResponse(dic, safe=False)


def GoogleAuthorize(request):
    if request.method=='POST':
        request_info = str(request.body, 'utf-8')
        user_info = json.loads(request_info)
        try:
            name = user_info['name']
            surname = user_info['surname']
            email = user_info['email']
            password = 'Google sign in'
        except:
            return HttpResponseBadRequest('Illegal arguments')

        if users.filter(email=email).count()!=0:
            user = users.get(email=email)
            tokken = tokkens.get(user=user)
            dic = {'tokken': tokken.user_tokken}
            json_response = JsonResponse(dic)
            return json_response
        else:
            new_user = User(users.all().count() + 1, name, surname, email, password)
            tokken = generationCodes.makeTokken()
            new_user.save()
            new_user_tokken = UserTokken(tokkens.all().count() + 1, tokken, new_user.id)
            new_user_tokken.save()
            dic = {'tokken': tokken}
            json_response = JsonResponse(dic)
            return json_response

    else:
        return Http404("Illegal method")


def FacebookAuthorize(request):
    if request.method == 'POST':
        request_info = str(request.body, 'utf-8')
        request_info = json.loads(request_info)
        try:
            access_token=request_info['access token']
        except:
            return HttpResponseBadRequest('Illegal arguments')

        try:
            rw = requests.get("https://graph.facebook.com/me?access_token="+access_token)
            user_info=json.loads(rw.text)
            name = user_info['name'].split(' ', 1)[0]
            surname = user_info['name'].split(' ', 1)[1]
            email = user_info['id']
            password = 'Facebook sign in'

        except:
            return HttpResponseBadRequest("Illegal auth code")
        if users.filter(email=email).count() != 0:
            user = users.get(email=email)
            tokken = tokkens.get(user=user)
            dic = {'tokken': tokken.user_tokken}
            json_response = JsonResponse(dic)
            return json_response
        else:
            new_user = User(users.all().count() + 1, name, surname, email, password)
            tokken = generationCodes.makeTokken()
            new_user.save()
            new_user_tokken = UserTokken(tokkens.all().count() + 1, tokken, new_user.id)
            new_user_tokken.save()
            dic = {'tokken': tokken}
            json_response = JsonResponse(dic)
            return json_response

    else:
        return Http404("Illegal method")