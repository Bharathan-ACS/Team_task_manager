from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.utils.timezone import now


# SIGNUP
def signup_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {
                'error': 'Username already exists'
            })

        User.objects.create_user(
            username=username,
            password=password,
            role=role
        )
        return redirect('/login/')
    return render(request, 'signup.html')


# LOGIN
def login_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {
                'error': 'Invalid username or password'
            })
    return render(request, 'login.html')


# LOGOUT
def logout_view(request):
    logout(request)
    return redirect('/login/')


# DASHBOARD
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    tasks = Task.objects.filter(
        assigned_to=request.user
    )
    completed = tasks.filter(
        status='done'
    ).count()
    overdue = tasks.filter(
        due_date__lt=now().date()
    ).exclude(status='done').count()
    return render(request, 'dashboard.html', {
        'tasks': tasks,
        'completed': completed,
        'overdue': overdue
    })

# CREATE PROJECT
def create_project(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    if request.user.role != 'admin':
        return redirect('/')

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        Project.objects.create(
            name=name,
            description=description,
            created_by=request.user
        )
        return redirect('/')
    return render(request, 'create_project.html')


# CREATE TASK
def create_task(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    projects = Project.objects.all()
    users = User.objects.all()

    if request.method == 'POST':

        Task.objects.create(
            title=request.POST.get('title'),
            project_id=request.POST.get('project'),
            assigned_to_id=request.POST.get('user'),
            due_date=request.POST.get('due_date')
        )

        return redirect('/')

    return render(request, 'create_task.html', {
        'projects': projects,
        'users': users
    })


# UPDATE TASK
def update_task(request, id):

    if not request.user.is_authenticated:
        return redirect('/login/')

    task = Task.objects.get(id=id)
    task.status = request.POST.get('status')
    task.save()
    return redirect('/')