from django.conf.urls import url

from . import views

urlpatterns= [
    # : /account_managment/
    url(r'^$',views.getUsers,name='getUsers'),
    # : /account_managment/addUser/
    url(r'^addUser/$',views.addUser,name='addUser'),
    # : /account_managment/authorizeUser/
    url(r'^authorizeUser/$',views.authorizeUser,name='authorizeUser'),
    #: /account_managment/getUserInfo,tokken=[токен]/
    url(r'^getUserInfo,tokken=(?P<tokken>.+)/$',views.getUserInfo,name='getUserInfo'),
    #: /account_managment/getPassword/
    url(r'^getPassword/$',views.getPassword,name='getPassword'),
    #: /account_managment/changePassword,tokken=[токен]/
    url(r'^changePassword,tokken=(?P<tokken>.+)/$',views.changePassword,name='changePassword'),
    url(r'^checkUserService/$',views.checkUserService,name='checkuserService'),
    url(r'^getAllUserServices,tokken=(?P<tokken>.+)/$',views.getAllUserServices,name='getAllUserServices'),

    url(r'^GoogleAuthorize/$',views.GoogleAuthorize,name='GoogleAuthorize'),

    url(r'FacebookAuthorize/$',views.FacebookAuthorize,name='FacebookAuthorize')

]