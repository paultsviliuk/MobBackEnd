#import tablib
from django.contrib import admin
from .models import User,UserServices,UserTokken,UserActivatedPromoCodes,UsersRequests
from import_export import resources, widgets, fields
from import_export.admin import ImportExportModelAdmin,ExportMixin, ImportMixin
#import django_filters
#from django_filters import rest_framework as filters
#from django.dispatch import receiver
#from import_export.signals import post_export


class RequestsAdmin(admin.ModelAdmin):
    list_display = ('date', 'requestChannel', 'problem', 'solution')

class UsersAdmin(admin.ModelAdmin):
    search_fields = ('name', 'email', 'telephone')


class RequestsInline(admin.StackedInline):
    model = UsersRequests
    extra = 3


class UserResource(resources.ModelResource):

    class Meta:
        model = User
        fields = ('name', 'surname', 'email', 'telephone', 'registration_date', 'activated_services', 'activated_promo_codes')
        export_order = ('name', 'surname', 'email', 'telephone', 'registration_date', 'activated_services', 'activated_promo_codes')

class ServicesResource(resources.ModelResource):

    class Meta:
        model = UserServices
        fields = ( 'user__name', 'user__surname', 'user__email', 'user__telephone', 'user__registration_date', 'service__id',
                   'service__service_name', 'end_time', 'user__activated_promo_codes')# 'RequestsInline__date', 'RequestsInline__requestChannel',
                   #'RequestsInline__problem', 'RequestsInline__solution')
        export_order = ('user__name', 'user__surname', 'user__email', 'user__telephone', 'user__registration_date', 'service__id',
                        'service__service_name', 'user__activated_promo_codes', 'end_time')

class UserRequestsResource(resources.ModelResource):
    class Meta:
        model = UsersRequests
        fields = ('username__name','username__surname', 'date', 'requestChannel', 'problem', 'solution')
        export_order = ('username__name','username__surname', 'date', 'requestChannel', 'problem', 'solution')


#class UsersResource(resources.ModelResource):
 #   class Meta:
  #      model = User
   #     fields = ('id', 'name', 'surname', 'email', 'telephone',
    #              'userRequest__date', 'userRequest__requestChannel', 'userRequest__problem', 'userRequest__solution')


#class UserAdmin(ImportExportModelAdmin):
#    resource_class = UsersResource


@admin.register(User)
class UserAdmin(ExportMixin,admin.ModelAdmin):
    resource_class = UserResource
    inlines = [RequestsInline]
    search_fields = ('name', 'surname', 'email', 'telephone', 'activated_promo_codes')


@admin.register(UserServices)
class ServiceAdmin(ExportMixin,admin.ModelAdmin):
    resource_class = ServicesResource


@admin.register(UsersRequests)
class UserRequestsAdmin(ExportMixin,admin.ModelAdmin):
    resource_class = UserRequestsResource

# Register your models here.
#admin.site.register(UsersRequests, UserRequestsAdmin)
#admin.site.register(User,UsersAdmin)UsersAdmin,
#admin.site.register(UserServices, ServiceAdmin)
#admin.site.register(UserTokken)
#admin.site.register(UserActivatedPromoCodes)




#class UserAdmin(ImportExportModelAdmin):
   # resource_class = UsersResource
    #list_display = ('id', 'name', 'email', 'telephone', 'userRequest__date', 'userRequest__requestChannel',
     #              'userRequest__problem', 'userRequest__solution')