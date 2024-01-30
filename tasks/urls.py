from .views import TasksView, NewTask, LoginView, logout_view, RegisterView, EditTaskView, MoveTaskForwardView, MoveTaskBackwardView, DeleteTaskView
from django.urls import path

urlpatterns = [
    path('', TasksView.as_view(), name='tasksview'),
    path('new/', NewTask.as_view(), name='newtask'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('edit_task/<int:task_id>/', EditTaskView, name='edit_task'),
    path('move-forward/<int:task_id>/', MoveTaskForwardView.as_view(), name='move_task_forward'),
    path('move-backward/<int:task_id>/', MoveTaskBackwardView.as_view(), name='move_task_backward'),
    path('delete/<int:task_id>/', DeleteTaskView.as_view(), name='delete_task'),
    ]
