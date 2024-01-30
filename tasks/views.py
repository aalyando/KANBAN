from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Task
from .forms import FormCreate, AuthenticationForm, RegisterForm, TaskForm
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class TasksView(View):
        def get(self, request):
            tasks = Task.objects.all()
            return render(request, 'tasks_list.html', {'tasks_list': tasks})


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class NewTask(View):
    def get(self, request):
        form = FormCreate()
        return render(request, 'new_task.html', {'form': form})

    def post(self, request):
        if request.method == 'POST':
            form = FormCreate(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                if request.user.is_superuser:
                    assigned_to = form.cleaned_data['assigned_to']
                    task.assigned_to = assigned_to
                else:
                    task.assigned_to = request.user
                task.save()
                return redirect('/')
        else:
            form = FormCreate()
        return render(request, 'new_task.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        if request.method == "POST":
            form = AuthenticationForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('authenticated_user')
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    
    def post(self, request):
        if request.method == 'POST':
            form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            form = RegisterForm()
            return render(request, 'register.html', {'form': form})


@login_required(login_url='/login/')
def EditTaskView(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    form = TaskForm(request.POST, instance=task, user=request.user)
    if form.is_valid():
        form.save()
        return redirect('/')
    form = TaskForm(instance=task, user=request.user)
    return render(request, 'edit_task.html', {'form': form, 'task': task})


class MoveTaskForwardView(View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        next_status = {'New': 'In Progress', 'In Progress': 'In QA', 'In QA': 'Ready', 'Ready': 'Done'}
        task.status = next_status.get(task.status, task.status)
        task.save()
        return redirect('/')


class MoveTaskBackwardView(View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        previous_status = {'In Progress': 'New', 'In QA': 'In Progress', 'Ready': 'In QA', 'Done': 'Ready'}
        task.status = previous_status.get(task.status, task.status)
        task.save()
        return redirect('/')


class DeleteTaskView(View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        if request.user.is_superuser:
            task.delete()
            return redirect('/')


def logout_view(request):
        logout(request)
        return redirect('/')