from django.urls import path
from .views import DashboardView, ProjectDetailView
from .views import TaskStatusUpdateView
from .views import TaskCreateView
from .views import TaskUpdateView
from .views import toggle_task_status


app_name = 'tasks'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('tasks/<int:pk>/status/', TaskStatusUpdateView.as_view(), name='task_status_update'),
    path("projects/<int:project_pk>/tasks/create/",TaskCreateView.as_view(),name="task_create"),
    path("tasks/<int:pk>/edit/",TaskUpdateView.as_view(),name="task_update"),
    path("tasks/<int:pk>/toggle/",toggle_task_status,name="task_toggle")
]