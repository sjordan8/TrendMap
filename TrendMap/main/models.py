from django.db import models

# Create your models here.
class Tokens(models.Model):
    key = models.CharField(max_length=250)
    secret = models.CharField(max_length=250)
