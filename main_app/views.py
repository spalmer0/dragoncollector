import uuid
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# Use sessions to log the user in
from django.contrib.auth import login
# Display user inputs in a form
from django.contrib.auth.forms import UserCreationForm
# login_required decorator:
from django.contrib.auth.decorators import login_required
# CBV use mixins instead of decorators
from django.contrib.auth.mixins import LoginRequiredMixin
# models, forms
from .models import Dragon, Toy, Photo
from .forms import FeedingForm
# format should be `protocol://service-code.region-code.amazonaws.com/`
S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'spalmer0-dragoncollector'

def signup(request):
    error_message = ''

    # if we have POST request, create form w/ data, login user
    if request.method == 'POST':
        # Create the user using the UserCreationForm
        form = UserCreationForm(request.POST)

        if form.is_valid():
            # actually save the user if our form data is valid
            user = form.save()
            # actually log the user in (session-based)
            login(request, user)
            return redirect('dragons_index')
        else:
            error_message = 'Invalid data for sign up'

    # if there's a bad POST request or normal GET request, send errors to the sign-up template
    form = UserCreationForm()
    context = { 'form': form, 'error_message': error_message }
    return render(request, 'registration/signup.html', context)

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def dragons_index(request):

    # dragons = Dragon.objects.all()
    # filter to find only dragons owned by the logged in user
    dragons = Dragon.objects.filter(user=request.user)
    return render(request, 'dragons/index.html', {'dragons': dragons })

@login_required
def dragons_detail(request, dragon_id):
    dragon = Dragon.objects.get(id=dragon_id)
    # Exclude from our query all toys associated with the current dragon
    toys_dragon_doesnt_have = Toy.objects.exclude(id__in = dragon.toys.all().values_list('id'))
    # instantiate FeedingForm to be rendered in the template
    feeding_form = FeedingForm()
    return render(request, 'dragons/detail.html',
        {'dragon': dragon, 'feeding_form': feeding_form,
        'available_toys': toys_dragon_doesnt_have
    })

@login_required
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

@login_required
def add_photo(request, dragon_id):
    # the <input> will have 'name' attribute - that's the key our file will be on the incoming data
    photo_file = request.FILES.get('photo_file', None)

    if photo_file:
        # create an s3 instance
        s3 = boto3.client('s3')

        # generate a unique "key" for the image
        # variable to store the index of the dot before the file extension
        # rfind will find the last instance of the '.' character
        index_of_last_period = photo_file.name.rfind('.')
        # generate a unique key & grab the first 6 characters
        # example: G4F&8F.png
        key = uuid.uuid4().hex[:6] + photo_file.name[index_of_last_period:]

        try:
            # s3 client - attempt to perform a file upload
            s3.upload_fileobj(photo_file, BUCKET, key)

            # Generate the URL based on the key name, our base url, bucket
            # example: https://s3.us-east-1.amazonaws.com/spalmer0-dragoncollector/G4F&8F.png
            url = f"{S3_BASE_URL}{BUCKET}/{key}"

            photo = Photo(url=url, dragon_id=dragon_id)
            photo.save()

        except:
            print('An error occurred uploading files to AWS')

    return redirect('dragons_detail', dragon_id=dragon_id)


class DragonCreate(LoginRequiredMixin, CreateView):
    model = Dragon
    fields = ['name', 'breed', 'description', 'age']

    # override form_valid to attach the user to the dragon
    # before form data is saved
    def form_valid(self, form):
        # the ddragon data will be stored in 'form.instance'
        # self.request.user will be the currently logged in user
        form.instance.user = self.request.user #allowing CreateView parent class to handle the rest
        return super().form_valid(form)

class DragonUpdate(LoginRequiredMixin, UpdateView):
    model = Dragon
    fields = ['breed', 'description', 'age']

class DragonDelete(LoginRequiredMixin, DeleteView):
    model = Dragon
    success_url = '/dragons/'

@login_required
def assoc_toy(request, dragon_id, toy_id):
    # Locate the dragon & '.add' the toy by its ID
    Dragon.objects.get(id=dragon_id).toys.add(toy_id)
    return redirect('dragons_detail', dragon_id=dragon_id)

@login_required
def unassoc_toy(request, dragon_id, toy_id):
    Dragon.objects.get(id=dragon_id).toys.remove(toy_id)
    return redirect('dragons_detail', dragon_id=dragon_id)

def toys_index(request):
    toys = Toy.objects.all()
    return render(request, 'toys/index.html', {'toys': toys })

def toys_detail(request, toy_id):
    toy = Toy.objects.get(id=toy_id)
    return render(request, 'toys/detail.html', {'toy': toy})

class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'

class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ['color', 'description']

class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'