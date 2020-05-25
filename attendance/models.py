from django.db import models

class Trooper(models.Model):
    name = models.CharField(max_length=255)
    platoon = models.IntegerField()

    def __str__(self):
        return self.name

class Absence(models.Model): 
    trooper = models.ForeignKey(Trooper, on_delete=models.CASCADE)
    remarks = models.TextField(default=None)
