from django.urls import path, include
from . import views


app_name = "todo"

urlpatterns = [
    # site urls
    path("", views.TodoView.as_view(), name="main_page"),
    path("add-day/<int:day>/", views.AddDayView.as_view(), name="add_day"),
    path(
        "add-month/<int:month>/",
        views.AddMonthView.as_view(),
        name="add_month",
    ),
    path(
        "add-level/<int:level>/",
        views.AddLevelView.as_view(),
        name="add_level",
    ),
    path(
        "clear-session/",
        views.ClearSessionView.as_view(),
        name="clear_session",
    ),
    path("create-task/", views.CreateTaskView.as_view(), name="create_task"),
    path(
        "done-task/<int:task_id>/",
        views.DoneTaskView.as_view(),
        name="done_task",
    ),
    path(
        "clear-completed-tasks/",
        views.ClearCompletedTaskView.as_view(),
        name="clear_tasks",
    ),
    # api v1 urls
    path("todo/api/v1/", include("todo.api.v1.urls", namespace="api_v1")),
]
