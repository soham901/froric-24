from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, EditProfileForm
from .models import BasicRoleDemo


@login_required
def profile(request):
    context = {
        'user': request.user,
    }
    
    return render(request, 'accounts/profile.html', context)


@login_required
def logout(request):
    auth.logout(request)
    return render(request, 'accounts/logout.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'accounts/edit.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a default role for the user
            BasicRoleDemo.objects.create(user=user)
            auth.login(request, user)
            return redirect('accounts:profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})
