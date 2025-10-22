from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView

from .forms import CustomUserCreationForm, SignUpForm, CustomUserForm
from django.contrib.auth.decorators import login_required, permission_required
from .models import CustomUser

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
            messages.info(request, "Tizimga muvaffaqiyatli kirdingiz!")
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

@login_required
def profile_view(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    return render(request, 'profile.html', {'user':user})
    # 'profile': user_profile, 'user':request.user


@login_required
def profile_edit_view(request, pk):
    profile = get_object_or_404(CustomUser, id=pk)

    # Ensure the logged-in user is editing their own profile
    if profile.id == request.user.id:
        if request.method == 'POST':
            form = CustomUserForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your profile has been updated successfully!')
                return redirect('index')
                # return redirect('profile', pk=request.user.pk)
        else:
            form = CustomUserForm(instance=profile)

        return render(request, 'profile_edit.html', {'form': form})

    else:
        # If user tries to edit someone else's profile, redirect or show a forbidden page
        return redirect('index')  # You can change this to an error page if needed



































