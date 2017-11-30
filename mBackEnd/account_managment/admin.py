from django.contrib import admin
from .models import User,UserServices,UserTokken

# Register your models here.
admin.site.register(User)
admin.site.register(UserServices)
admin.site.register(UserTokken)


