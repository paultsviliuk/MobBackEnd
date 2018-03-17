from django.contrib import admin
from import_export.admin import ImportMixin,ImportExportModelAdmin
from import_export import resources
from .models import Services,PromoCodes,ServicesCosts,CauseOfReservedPromocodes,ActivatedType
# Register your models here.


class PromocodesResource(resources.ModelResource):

    class Meta:
        model = PromoCodes
        skip_unchanged = True
        report_skipped = False
        fields = ('id', 'promo_code', 'duration', 'service', 'cause_of_reservation')

@admin.register(PromoCodes)
class PromocodesAdmin(ImportMixin,admin.ModelAdmin):
    resource_class = PromocodesResource


admin.site.register(Services)
#admin.site.register(PromoCodes, PromocodesAdmin)
admin.site.register(ServicesCosts)
admin.site.register(CauseOfReservedPromocodes)
#admin.site.register(ActivatedType)