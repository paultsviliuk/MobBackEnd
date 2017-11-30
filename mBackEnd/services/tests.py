import requests
import json


def TestActivatePromoCode(promo_code,tokken):

     dic={
          "promo code" : promo_code ,
          "tokken" : tokken
          }
     r=requests.post(r"http://127.0.0.1:8000/services/activatePromoCode/",json=json.dumps(dic))
     print(r.text)

def TestActivateService(tokken,service_id,duration):
     dic = {
          "tokken": tokken,
          "service id": service_id,
          "duration": duration
     }
     r = requests.post(r"http://127.0.0.1:8000/services/activateService/", json=json.dumps(dic))
     print(r.text)


def TestCheckServiceForBuying(tokken,service_id,duration):
     dic = {
          "tokken": tokken,
          "service id": service_id,
          "duration": duration
     }
     r = requests.post(r"http://127.0.0.1:8000/services/checkServiceForBuying/", json=json.dumps(dic))
     print(r.text)


def TestGetAllServices():
     r = requests.get(r"http://127.0.0.1:8000/services/getAllServices/")
     print(r.text)

def TestCheckPromoCodeIsExist(service_id,duration):
     dic = {
          "service id": service_id,
          "duration": duration
     }
     r = requests.post(r"http://127.0.0.1:8000/services/checkPromoCodeIsExist/", json=json.dumps(dic))
     print(r.text)

def TestGetPromoCode(tokken,service_id,duration):
     dic = {
          "tokken": tokken,
          "service id": service_id,
          "duration": duration
     }
     r = requests.post(r"http://127.0.0.1:8000/services/getPromocode/", json=json.dumps(dic))
     print(r.text)




TestGetAllServices()
TestActivateService("(b<>'>x80l>xa4v>xbbX,*<)",'4','12')
TestCheckPromoCodeIsExist('4','12')
TestGetPromoCode("(b<>'>x80l>xa4v>xbbX,*<)",'4','6')
