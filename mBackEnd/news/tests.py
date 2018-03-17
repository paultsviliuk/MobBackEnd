import requests
import json


def TestGetAllNews():
    r=requests.get(r"http://127.0.0.1:8000/news/getAllNews/")
    print(r.text)

def TestGetLastNews():
    r=requests.get(r"http://127.0.0.1:8000/news/getLastNews")
    print(r.text)

TestGetAllNews()
TestGetLastNews()