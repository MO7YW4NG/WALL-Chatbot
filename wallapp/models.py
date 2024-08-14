from django.db import models

# Create your models here.
class history(models.Model):
    user = models.CharField(null=False,default="",max_length=33)
    ans1 = models.TextField(null=False)
    q1 = models.TextField(null=False)
    ans2 = models.TextField(null=False)
    q2 = models.TextField(null=False)
    ans3 = models.TextField(null=False)
    sum = models.TextField(null=False)
    score = models.FloatField(null=False,default=0)
    def __str__(self):
        return str(self.score)

class qanda(models.Model):
    question = models.TextField(null=False)
    answer = models.TextField(null=False)
    def __str__(self):
        return str(self.id)

class school(models.Model):
    name = models.TextField(null=False)
    info = models.TextField(null=False)
    def __str__(self):
        return str(self.id)