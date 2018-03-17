from django.db import models
from django.db.models.signals import post_delete,pre_save

# Create your models here.

class ActivatedType(models.Model):
    type=models.CharField(max_length=15,primary_key=True)

    def __str__(self):
        return self.type

class Services(models.Model):
    id=models.PositiveIntegerField(primary_key=True)
    image=models.ImageField()
    service_name=models.CharField(max_length=50)
    description=models.CharField(max_length=200)
    activated_type=models.ForeignKey(ActivatedType,on_delete=models.CASCADE)

    def __str__(self):
        return self.service_name+" "+self.description+" "

    def delete_Services_content(sender, **kwargs):
        mf = kwargs.get("instance")
        try:
            mf.image.delete(save=False)
        except :
            pass

    def delete_same_object(sender,**kwargs):
        try:
            mf=kwargs.get("instance")
            for ds in Services.objects.filter(image=mf.image,service_name=mf.service_name,description=mf.description,activated_type=mf.activated_type):
                for sc in ServicesCosts.objects.filter(service=ds):
                    sc.service=mf
                    sc.save()
                for pm in PromoCodes.objects.filter(service=ds):
                    pm.service=mf
                    pm.save()
                ds.delete()
        except:
            pass

    pre_save.connect(delete_same_object)
    post_delete.connect(delete_Services_content)

class ServicesCosts(models.Model):
    service=models.ForeignKey(Services,on_delete=models.CASCADE)
    price=models.IntegerField()
    duration=models.IntegerField()

    def __str__(self):
        return str(self.service)+str(self.price)

class CauseOfReservedPromocodes(models.Model):
    cause=models.CharField(max_length=50,primary_key=True)

    def __str__(self):
        return self.cause

class PromoCodes(models.Model):
    promo_code=models.CharField(max_length=50,unique=True)
    duration=models.IntegerField(max_length=20)
    service=models.ForeignKey(Services,blank=True,null=True,on_delete=models.CASCADE)
    cause_of_reservation=models.ForeignKey(CauseOfReservedPromocodes,blank=True,null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.promo_code+" "+str(self.service)