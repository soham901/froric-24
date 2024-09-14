from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')