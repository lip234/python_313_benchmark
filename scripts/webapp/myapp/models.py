from django.db import models

# Create your models here.

class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    pub_date = models.DateTimeField('date published')
    author = models.CharField(max_length=100)
