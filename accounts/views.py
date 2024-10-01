from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, SignUpForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Siz muvaffaqiyatli ro`yhatdan o`tdingiz!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})

    return render(request, 'register.html', {'form':form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Tizimga muvaffaqiyatli kirdingiz!")
            return redirect('index')
        else:
            messages.warning(request, "Tizimga kirib bo`lmadi!")
            return redirect('login')
    else:
        return render(request, 'registration/login.html', )


def logout_user(request):
    logout(request)
    messages.success(request, "Tizimdan chiqdingiz!")
    return redirect('index')


def profile_view(request):

    if request.user.is_authenticated:
        return render(request, 'profile.html')


def profile_edit_view(request):
    pass




































