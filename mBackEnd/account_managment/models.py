from django.db import models
from services.models import Services
# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=200)
    surname=models.CharField(max_length=200)
    email=models.EmailField()
    password=models.CharField(max_length=200)
    telephone=models.PositiveIntegerField(max_length=12,blank=True,null=True)

    def __str__(self):
        return self.name+" "+self.surname+" "

class UserTokken(models.Model):
    user_tokken=models.CharField(max_length=30)
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)+" "+self.user_tokken+" "

class UserServices(models.Model):
    service=models.ForeignKey(Services,on_delete=models.CASCADE,primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    end_time = models.DateField('end time')

    def __str__(self):
        return str(self.user)+" "+str(self.service)