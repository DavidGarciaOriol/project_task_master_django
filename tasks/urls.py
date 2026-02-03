from django.urls import path
from .views import DashboardView, ProjectDetailView
from .views import TaskStatusUpdateView


app_name = 'tasks'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('tasks/<int:pk>/status/', TaskStatusUpdateView.as_view(), name='task_status_update'),
]