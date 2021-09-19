from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    pass

# https://ru.wikipedia.org/wiki/TF-IDF
class Word(models.Model):
    word = models.CharField(max_length=150, unique=True) 
    counter = models.IntegerField(default=0)   # кол-во раз это слово употребленно во всех текстах (не distinct)
    idf_ammount = models.IntegerField(default=1)  # уникальное (distinct) кол-во раз это слово встречается во всех документах
    idf = models.FloatField(default=0) # реальный idf вычесленный логарифрм
    
    
    
    def __str__(self):
        return (f"{self.word} : {self.counter}")


class Query_name(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    time_created = models.DateTimeField(default=timezone.now)
    query_title = models.CharField(max_length = 250)    
    
    def __str__(self):
        return (f"title: {self.query_title}, by: {self.username}")


class Query_name_Words(models.Model):
    word_id = models.ForeignKey(Word, on_delete=models.CASCADE)
    query_name_id = models.ForeignKey(Query_name, on_delete=models.CASCADE)
    counter = models.IntegerField(default=0) 

    def __str__(self):
        return (f"{self.word_id}, {self.query_name_id}, counter:{self.counter}")
    

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/')

    def __str__(self):
        return (f"{self.docfile}")
