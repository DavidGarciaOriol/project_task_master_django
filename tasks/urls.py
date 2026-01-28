from django.urls import path
from .views import DashboardView, ProjectDetailView

app_name = 'tasks'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project_detail')
]