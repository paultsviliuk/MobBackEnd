from django.db import models
from services.models import Services,PromoCodes,CauseOfReservedPromocodes
# Create your models here.

class User(models.Model):
    name=models.CharField(max_length=200)
    surname=models.CharField(max_length=200)
    email=models.EmailField()
    password=models.CharField(max_length=200)
    telephone=models.PositiveIntegerField(max_length=12,blank=True,null=True)
    activated_services = models.CharField(max_length=1000, blank=True, null=True)
    activated_promo_codes=models.CharField(max_length=1000,blank=True,null=True)
    registration_date=models.DateField('registration date',null=True)

    def __str__(self):
        return self.name + " " + self.surname


class UsersRequests(models.Model):
    date = models.DateField()
    #promocode = models.OneToOneField('UserActivatedPromoCodes', primary_key=True)
    username=models.ForeignKey(User, on_delete=models.CASCADE)
    requestChannel = models.CharField(max_length=30)
    problem = models.CharField(max_length=200)
    solution = models.CharField(max_length=200)

    def __str__(self):
        table = ""
        table = str(self.date) + " " + str(self.username) + " " + str(self.requestChannel) + " " + str(self.problem) + " " + str(self.solution)
        return table

    def save_UsersRequests_content(sender, **kwargs):
        mf = kwargs.get("instance")
        try:
            for ds in UsersRequests.objects.filter(pk=mf.id):
                ds.save()
                return ds
        except :
            pass


class UserTokken(models.Model):
    user_tokken=models.CharField(max_length=30)
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)+" "+self.user_tokken+" "


class UserServices(models.Model):
    service=models.ForeignKey(Services,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    end_time = models.DateField('end time')

    def __str__(self):
        return str(self.user)+" "+str(self.service)


class UserActivatedPromoCodes(models.Model):
    user_service=models.ForeignKey(UserServices,on_delete=models.CASCADE)
    promo_code = models.CharField(max_length=50, primary_key=True)
    duration = models.IntegerField(max_length=20)
    cause_of_reservation = models.ForeignKey(CauseOfReservedPromocodes, blank=True, null=True,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user_service)