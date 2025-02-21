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
    # Получаем параметры фильтрации
    status_filter = request.GET.get('status')
    date_sort = request.GET.get('date_sort')
    
    # Базовый QuerySet для проблем пользователя
    user_problems = Problem.objects.filter(user=request.user)
    
    # Применяем фильтр по статусу
    if status_filter:
        user_problems = user_problems.filter(status=status_filter)
    
    # Применяем сортировку по дате
    if date_sort == 'asc':
        user_problems = user_problems.order_by('created_at')
    else:
        user_problems = user_problems.order_by('-created_at')
    
    if request.user.is_staff:
        # Для администратора также фильтруем все проблемы
        all_problems = Problem.objects.all()
        if status_filter:
            all_problems = all_problems.filter(status=status_filter)
        if date_sort == 'asc':
            all_problems = all_problems.order_by('created_at')
        else:
            all_problems = all_problems.order_by('-created_at')
            
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
                
                # Проверяем, не является ли заявка уже решенной или отклоненной
                if problem.status in ['solved', 'rejected']:
                    messages.error(request, 'Нельзя изменить статус решенной или отклоненной заявки')
                    return redirect('lk')
                    
                form = ProblemUpdateForm(request.POST, request.FILES, instance=problem)
                
                if form.is_valid():
                    new_status = form.cleaned_data['status']
                    
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
            'user': request.user,
            'user_problems': user_problems,
            'all_problems': all_problems,
            'categories': categories,
            'category_form': category_form,
            'problem_update_form': ProblemUpdateForm(),
            'current_status': status_filter,
            'current_date_sort': date_sort,
        }
    else:
        context = {
            'user': request.user,
            'user_problems': user_problems,
            'current_status': status_filter,
            'current_date_sort': date_sort,
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

from django.http import JsonResponse
from .models import Problem  

def delete_application(request, application_id):
    if request.method == 'DELETE':
        try:
            problem = Problem.objects.get(id=application_id)
            # Проверяем статус заявки
            if problem.status in ['solved', 'rejected']:
                return JsonResponse({'message': 'Нельзя удалить решенную или отклоненную заявку'}, status=403)
            problem.delete()
            return JsonResponse({'message': 'Заявка удалена'}, status=200)
        except Problem.DoesNotExist:
            return JsonResponse({'message': 'Заявка не найдена'}, status=404)
    return JsonResponse({'message': 'Метод не разрешен'}, status=405)