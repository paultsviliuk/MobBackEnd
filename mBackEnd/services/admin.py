from django.contrib import admin
from .models import Services,PromoCodes,ServicesCosts
# Register your models here.

admin.site.register(Services)
admin.site.register(PromoCodes)
admin.site.register(ServicesCosts)