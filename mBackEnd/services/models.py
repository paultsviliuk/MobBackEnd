from django.db import models
from django.db.models.signals import post_delete

# Create your models here.

class Services(models.Model):
    image=models.ImageField()
    service_name=models.CharField(max_length=50)
    description=models.CharField(max_length=200)


    def __str__(self):
        return self.service_name+" "+self.description+" "

    def delete_Services_content(sender, **kwargs):
        mf = kwargs.get("instance")
        try:
            mf.image.delete(save=False)
        except :
            pass

    post_delete.connect(delete_Services_content)

class ServicesCosts(models.Model):
    service=models.ForeignKey(Services,on_delete=models.CASCADE)
    price=models.IntegerField()
    duration=models.IntegerField()

class PromoCodes(models.Model):
    promo_code=models.CharField(max_length=50,primary_key=True)
    duration=models.IntegerField(max_length=20)
    service=models.ForeignKey(Services,on_delete=models.CASCADE)

    def __str__(self):
        return self.promo_code+" "+str(self.service)
