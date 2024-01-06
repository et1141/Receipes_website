from django.db import models
from django.contrib.auth.models import User

#important!! in my models I'm using id_... (id_user e.g.), however those fields are not id's, they are django model objets. 
class Category(models.Model):
    name = models.CharField(max_length=255)
    img = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class RatesCategory(models.Model):
    score = models.IntegerField()
    id_user = models.ForeignKey(User, on_delete=models.CASCADE) ##i put here id but basicly it's an object
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.id_user.username} - {self.id_category.name} - {self.score}"

class Receipt(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()
    id_author = models.ForeignKey(User, on_delete=models.CASCADE)
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE,default=1)
    img = models.CharField(max_length=255)
    ingredients = models.JSONField()
    def __str__(self):
        return self.name
    
class RatesReceipt(models.Model):
    score = models.IntegerField()
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_receipt = models.ForeignKey(Receipt,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.id_user.username} - {self.id_receipt.name} - {self.score}"

