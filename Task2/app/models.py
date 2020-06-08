from django.db import models

class UserModel(models.Model):
    username = models.CharField(max_length=20,primary_key=True)
    password = models.CharField(max_length=20)

class ArticleModel(models.Model):
    at = (('Public', 'Public'), ('Private', 'Private'))
    username = models.CharField(max_length=20)
    topic_name =models.CharField(max_length=100)
    image = models.ImageField(upload_to='article_images/')
    description = models.CharField(max_length=10000)
    article_type = models.CharField(max_length=7,choices=at)
