from django.db import models
from django.urls import reverse

class Dragon(models.Model):
    name = models.CharField(max_length=250)
    breed = models.CharField(max_length=250)
    description = models.TextField(max_length=250)
    age = models.IntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('dragons_detail', kwargs={'dragon_id': self.id})


class Toy(models.Model):
    name = models.CharField(max_length=250)
    color = models.CharField(max_length=250)
    description = models.TextField(max_length=250)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('toys_detail', kwargs={'toy_id': self.id})

