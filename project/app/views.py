from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm, ProblemForm
from django.shortcuts import render
from .models import Problem
from django.http import JsonResponse

def index(request):
    solved_problems = Problem.objects.filter(is_solved=True).order_by('-timestamp')[:4]
    solved_count = Problem.objects.filter(is_solved=True).count()
    return render(request, 'app/index.html', {
        'solved_problems': solved_problems,
        'solved_count': solved_count,
    })

def get_solved_count(request):
    count = Problem.objects.filter(is_solved=True).count()
    return JsonResponse({'count': count})

@login_required
def create_application(request):
    if request.method == "POST":
        form = ProblemForm(request.POST, request.FILES)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.user = request.user
            problem.save()
            return redirect('lk')
    else:
        form = ProblemForm()
    return render(request, 'app/Create_application.html', {'form': form})

@login_required
def lk(request):
    user_problems = Problem.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'app/Lk.html', {'problems': user_problems})

def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegistrationForm()
    return render(request, 'app/registration.html', {'form': form})

def authorization(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'app/authorization.html', {'form': form})

def our_application(request):
    return render(request, 'app/our_application.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')
    return render(request, 'app/logout.html')