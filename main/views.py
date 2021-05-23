from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import re
from .models import *
from .forms import *
from .filters import *


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect')
        context = {}
        return render(request, 'main/login.html', context)


def logout_page(request):
    logout(request)
    return redirect('login')


def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        error_msg = ''
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            # if form.is_valid():
            #     form.save()
            #     username = form.cleaned_data.get('username')
            #     messages.success(request, 'Account created for ' + username + ' successfully')
            #     return redirect('login')

            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$"
            pat = re.compile(reg)
            mat = re.search(pat, password1)
            user_by_name = User.objects.filter(username=username)

            if user_by_name.exists():
                error_msg = 'Account already exists !'
            elif password1 != password2:
                error_msg = 'Passwords do not match !'
            elif not mat:
                error_msg = 'Password should have number, uppercase, lowercase, special symbol and from 8 chacracters long'
            else:
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, 'Account created for ' + username + ' successfully')
                return redirect('login')

        context = {'form':form,
                    'error_msg':error_msg,
        }
        return render(request, 'main/register.html', context)


@login_required(login_url='login')
def home(request):
    #tasks = Task.objects.all()
    tasks = request.user.task_set.all()
    #print('task theo user : ', tasks1)
    form = TaskForm()
    my_filter = TaskFilter(request.GET, queryset=tasks)
    #search_key = my_filter.data.get('name')
    tasks = my_filter.qs

    context = {'tasks':tasks, 
                'form':form,
                'my_filter':my_filter,
                # 'search_key':search_key
                }
    return render(request, 'main/list.html', context)


@login_required(login_url='login')
def create_task(request):
    #user = request.user
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # form.save()
            data = dict.copy(form.cleaned_data)
            data.update({'user': request.user})
            Task.objects.create(**data)
        return redirect('home')
    context = {'form':form}
    return render(request, 'main/create_task.html', context)


@login_required(login_url='login')
def detail_task(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    context = {'form':form}
    return render(request, 'main/detail_task.html', context)


@login_required(login_url='login')
def update_task(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid:
            form.save()
        return redirect('home')
    context = {'form':form}
    return render(request, 'main/update_task.html', context)


@login_required(login_url='login')
def delete_task(request, pk):
    item = Task.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('home')
    context = {'item':item}
    return render(request, 'main/delete_task.html', context)