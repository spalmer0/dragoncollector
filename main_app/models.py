from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner'),
)

class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)
    description = models.TextField(max_length=250)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('toys_detail', kwargs={'toy_id': self.id})

class Dragon(models.Model):
    name = models.CharField(max_length=250)
    breed = models.CharField(max_length=250)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    toys = models.ManyToManyField(Toy)

    # ownership field (relationship to the user)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('dragons_detail', kwargs={'dragon_id': self.id})


class Feeding(models.Model):
    date = models.DateField('feeding date')
    meal = models.CharField(
        max_length=1,
        choices=MEALS,
        default=MEALS[0][0]

    )

    dragon = models.ForeignKey(Dragon, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.get_meal_display()} at {self.date}"

    class Meta:
        ordering = ['-date']



class Photo(models.Model):
    # store the URL of the image on AWS
    url = models.CharField(max_length=200)
    # Relationship to the dragon
    dragon = models.ForeignKey(Dragon, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for dragon id #{self.dragon_id} @ {self.url}"