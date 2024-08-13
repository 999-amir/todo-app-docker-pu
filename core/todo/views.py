from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import TodoModel
from .cart import TodoTaskSession
from django.contrib import messages
from .forms import TaskForm
from datetime import datetime
from accounts.context_processors import profile_information


class TodoView(View):
    def get(self, request):
        try:
            tasks_done = TodoModel.objects.filter(profile__user=request.user, is_done=True).order_by('-updated')
            tasks_active = TodoModel.objects.filter(profile__user=request.user, is_done=False).order_by('dead_end')
        except TypeError:
            tasks_done = {}
            tasks_active = {}
        todo_task_session = TodoTaskSession(request)

        context = {
            'calender_days_name': ['Su', 'Mo', 'Tu', 'We', 'Te', 'Fr', 'Sa'],
            'calender_days_number': range(1, 32),
            'levels': ['green', 'orange', 'red'],
            'calender_months': ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'agu',
                                'sep', 'oct', 'nov', 'dec'],
            'tasks_done': tasks_done,
            'tasks_active': tasks_active,
            'todo_task': todo_task_session.todo_task
        }
        return render(request, 'todo/todo.html', context)


class AddDayView(View):
    def get(self, request, day: int):
        if 1 <= day <= 31:
            todo_task_session = TodoTaskSession(request)
            todo_task_session.add_day(day)
        else:
            messages.warning(request, 'day number should be between 1 and 31', 'red-600')
        return redirect('todo:main_page')


class AddMonthView(View):
    def get(self, request, month: int):
        if 1 <= month <= 12:
            todo_task_session = TodoTaskSession(request)
            todo_task_session.add_month(month)
        else:
            messages.warning(request, 'month number should be between 1 and 12')
        return redirect('todo:main_page')


class AddLevelView(View):
    def get(self, request, level: int):
        if 1 <= level <= 3:
            todo_task_session = TodoTaskSession(request)
            todo_task_session.add_level(level)
        else:
            messages.warning(request, 'level number should be between 1 and 3')
        return redirect('todo:main_page')


class ClearSessionView(View):
    def get(self, request):
        todo_task_session = TodoTaskSession(request)
        todo_task_session.clear_session()
        return redirect('todo:main_page')


class CreateTaskView(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'need registration', 'rose-600')
            return redirect('todo:main_page')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            todo_task = TodoTaskSession(request).todo_task
            month, day, task_level = todo_task['month'], todo_task['day'], todo_task['level']
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.cleaned_data['task']
                time = f'{month}/{day}/{datetime.today().year}'
                if task_level == 1:
                    level = 'green'
                elif task_level == 2:
                    level = 'orange'
                else:
                    level = 'red'
                TodoModel.objects.create(
                    profile_id=profile_information(request)['profile'].id,
                    level=level,
                    job=task,
                    dead_end=datetime.strptime(time, '%m/%d/%Y')
                )
        except KeyError:
            messages.warning(request, 'select month, day, level', 'red-600')
        return redirect('todo:main_page')


class DoneTaskView(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'need registration', 'rose-600')
            return redirect('todo:main_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, task_id: int):
        task = get_object_or_404(TodoModel, profile_id=profile_information(request)['profile'].id, id=task_id)
        task.is_done = True
        task.save()
        return redirect('todo:main_page')


class ClearCompletedTaskView(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'need registration', 'rose-600')
            return redirect('todo:main_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        tasks = TodoModel.objects.filter(profile_id=profile_information(request)['profile'].id, is_done=True)
        tasks.delete()
        messages.success(request, 'tasks removed', 'cyan-600')
        return redirect('todo:main_page')
