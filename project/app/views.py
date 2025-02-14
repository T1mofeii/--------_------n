from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm, ProblemForm, CategoryForm, ProblemUpdateForm
from django.shortcuts import render
from .models import Problem, Category
from django.http import JsonResponse
from django.contrib import messages

def index(request):
    # Получаем 4 последние решенные заявки
    solved_problems = Problem.objects.filter(status='solved').order_by('-created_at')[:4]
    solved_count = Problem.objects.filter(status='solved').count()
    
    return render(request, 'app/index.html', {
        'solved_problems': solved_problems,
        'solved_count': solved_count
    })

def get_solved_count(request):
    count = Problem.objects.filter(status='solved').count()
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
    user_problems = Problem.objects.filter(user=request.user)
    
    if request.user.is_staff:
        all_problems = Problem.objects.all().order_by('-created_at')
        categories = Category.objects.all()
        
        if request.method == 'POST':
            if 'category_form' in request.POST:
                category_form = CategoryForm(request.POST)
                if category_form.is_valid():
                    category_form.save()
                    return redirect('lk')
            elif 'problem_update' in request.POST:
                problem_id = request.POST.get('problem_id')
                problem = Problem.objects.get(id=problem_id)
                form = ProblemUpdateForm(request.POST, request.FILES, instance=problem)
                
                if form.is_valid():
                    new_status = form.cleaned_data['status']
                    
                    # Проверяем только для отклонения причину
                    if new_status == 'rejected' and not form.cleaned_data.get('rejection_reason'):
                        messages.error(request, 'Для отклонения заявки необходимо указать причину')
                        return redirect('lk')
                    
                    form.save()
                    messages.success(request, 'Статус заявки успешно обновлен')
                    return redirect('lk')
            elif 'delete_category' in request.POST:
                category_id = request.POST.get('category_id')
                Category.objects.filter(id=category_id).delete()
                return redirect('lk')
        
        category_form = CategoryForm()
        context = {
            'user_problems': user_problems,
            'all_problems': all_problems,
            'categories': categories,
            'category_form': category_form,
            'problem_update_form': ProblemUpdateForm(),
        }
    else:
        context = {
            'user_problems': user_problems,
        }
    
    return render(request, 'app/Lk.html', context)

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