from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RegistrationForm
from .models import UserProfile

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            birth_date = form.cleaned_data['birth_date']
            email = form.cleaned_data['email']


            user = User.objects.create_user(username=username, password=password, email=email)
            UserProfile.objects.create(user=user, birth_date=birth_date, email=email)

            return redirect('success')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def success(request):
    return render(request, 'succes.html')

