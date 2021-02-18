from django.db import models
from django.urls import reverse

MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner'),
)

class Toy(models.Model):
    name = models.CharField(max_length=250)
    color = models.CharField(max_length=250)
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