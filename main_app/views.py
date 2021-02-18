from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Dragon, Toy
from .forms import FeedingForm


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def dragons_index(request):
    dragons = Dragon.objects.all()
    return render(request, 'dragons/index.html', {'dragons': dragons })

def dragons_detail(request, dragon_id):
    dragon = Dragon.objects.get(id=dragon_id)
    feeding_form = FeedingForm()
    return render(request, 'dragons/detail.html',
    {'dragon': dragon, 'feeding_form': feeding_form})

def add_feeding(request, dragon_id):
    # create the ModelForm using the data in request.POST
    form = FeedingForm(request.POST)
    # validate the form
    if form.is_valid():
        # don't save the form to the db until it has the dragon_id assigned
        new_feeding = form.save(commit=False)
        # Attach the dragon_id to the feeding BEFORE saving it to the db
        new_feeding.dragon_id = dragon_id
        new_feeding.save()
    return redirect('dragons_detail', dragon_id=dragon_id)

class DragonCreate(CreateView):
    model = Dragon
    fields = '__all__'

class DragonUpdate(UpdateView):
    model = Dragon
    fields = ['breed', 'description', 'age']

class DragonDelete(DeleteView):
    model = Dragon
    success_url = '/dragons/'

def toys_index(request):
    toys = Toy.objects.all()
    return render(request, 'toys/index.html', {'toys': toys })

def toys_detail(request, toy_id):
    toy = Toy.objects.get(id=toy_id)
    return render(request, 'toys/detail.html', {'toy': toy})

class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'

class ToyUpdate(UpdateView):
    model = Toy
    fields = ['color', 'description']

class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'