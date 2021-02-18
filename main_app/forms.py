from django.forms import ModelForm
from .models import Feeding

# FeedingForm inherits from ModelForm
class FeedingForm(ModelForm):
    class Meta:
        model = Feeding
        fields = ['date', 'meal']