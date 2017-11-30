from django.db import models
from django.db.models.signals import post_delete

# Create your models here.

class News(models.Model):
    news_name=models.CharField(max_length=50)

    news_information=models.CharField(max_length=550)
    news_image=models.ImageField()

    def __str__(self):
        return self.news_name

    def delete_News_content(sender, **kwargs):
        mf = kwargs.get("instance")
        try:
            mf.news_image.delete(save=False)
        except :
            pass

    post_delete.connect(delete_News_content)