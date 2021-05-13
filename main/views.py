from django.shortcuts import render, redirect
from .models import *
from .forms import *

def home(request):
    tasks = Task.objects.all()

    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('home')

    context = {'tasks':tasks, 'form':form}
    return render(request, 'main/list.html', context)


def update_task(request, pk):
    task = Task.objects.get(id=pk)

    form = TaskForm(instance=task)

    context = {'form':form}

    return render(request, 'main/update_task.html', context)
