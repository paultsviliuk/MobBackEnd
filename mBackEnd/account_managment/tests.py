import requests,json


def TestAddUser(name,surname,email,password,telephone):
    dic={
        "name" : name,
        "surname" : surname,
        "email" : email,
        "password" : password,
        "telephone" : telephone
         }
    r=requests.post("http://127.0.0.1:8000/account_managment/addUser/",data=json.dumps(dic))
    print(r.text)

def TestGetUserInfo(tokken):
    r = requests.get("http://127.0.0.1:8000/account_managment/getUserInfo,tokken="+tokken)
    print(r.text)

def TestAuthorizeUser(email,password,telephone):
    dic = {
        "email": email,
        "password": password,
        "telephone": telephone
    }
    r = requests.post("http://127.0.0.1:8000/account_managment/authorizeUser/",data=json.dumps(dic))
    print(r.text)

def TestGetAllUserServices(tokken):
    r=requests.get("http://127.0.0.1:8000/account_managment/getAllUserServices,tokken="+tokken)
    print(r.text)


def TestGetpassword(email="",telephone=""):
    dic = {
        "email": email,
        "telephone": telephone
    }
    r=requests.post("http://127.0.0.1:8000/account_managment/getPassword/",data=json.dumps(dic))
    print(r.text)


TestAddUser("Alan","Velonas",email="leshiy12345678@gmail.com",password="11112",telephone="12345")
TestAuthorizeUser(email="leshiy12345678@gmail.com",password="11112",telephone="")
TestGetUserInfo("(b'>xaf(>x84>x99n>xc8>x96`>xc2')")
TestGetAllUserServices("(b'>xaf(>x84>x99n>xc8>x96`>xc2')")
#TestGetpassword(telephone="12345")


TestAddUser("Alan","Velonas","alan2@mail.ru","1111","1234")
TestGetUserInfo("(b<>'>x80l>xa4v>xbbX,*<)")
TestAuthorizeUser("alan2@mail.ru","1111","1234")
TestGetAllUserServices("(b<>'>x80l>xa4v>xbbX,*<)")

