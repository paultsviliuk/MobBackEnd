import requests
import json


def TestActivatePromoCode(promo_code,tokken):
     dic={
          "promo code" : promo_code ,
          "tokken" : tokken
          }
     r=requests.post(r"http://127.0.0.1:8000/services/activatePromoCode/",data=json.dumps(dic))
     print(r.text)

def TestActivateService(tokken,service_id,duration):
     dic = {
          "tokken": tokken,
          "service id": service_id,
          "duration": duration
     }
     r = requests.post(r"http://127.0.0.1:8000/services/activateService/", data=json.dumps(dic))
     print(r.text)


def TestCheckServiceForBuying(tokken,service_id,duration):
     dic = {
          "tokken": tokken,
          "service id": service_id,
          "duration": duration
     }
     r = requests.post(r"http://127.0.0.1:8000/services/checkServiceForBuying/", data=json.dumps(dic))
     print(r.text)


def TestGetAllServices():
     r = requests.get(r"http://127.0.0.1:8000/services/getAllServices/")
     print(r.text)

def TestCheckPromoCodeIsExist(service_id,duration):
     dic = {
          "service id": service_id,
          "duration": duration
     }
     r = requests.post(r"http://127.0.0.1:8000/services/checkPromoCodeIsExist/", data=json.dumps(dic))
     print(r.text)

def TestGetPromoCode(tokken,service_id,duration):
     dic = {
          "tokken": tokken,
          "service id": service_id,
          "duration": duration
     }
     r = requests.post(r"http://127.0.0.1:8000/services/getPromocode/", data=json.dumps(dic))
     print(r.text)

TestGetAllServices()
TestCheckServiceForBuying("(b'>xaf(>x84>x99n>xc8>x96`>xc2')",20,3)
TestActivateService("(b'>xaf(>x84>x99n>xc8>x96`>xc2')",20,3)
#TestActivatePromoCode("da","(b'khz>xa3>xc1>t>x08>xc4o')")
