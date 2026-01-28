from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count, Q
from django.views.generic import DetailView
from .mixins import ProjectAccessMixin
from .models import Project


from .models import Project, Task

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'tasks/dashboard.html'

    def get_context_data(self, **kwargs):
        """
        Obtenemos los datos del contexto para mostrar en la vista del Dashboard
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Estado de una tarea
        task_stats = Count(
            'tasks',
            distinct=True
        )

        # Contador de tareas
        done_tasks = Count(
            'tasks',
            filter=Q(tasks__status=Task.Status.DONE),
            distinct=True
        )

        # Configuramos el contexto para mostrar los proyectos propietarios
        context['owned_projects'] = (
            Project.objects
            .filter(owner=user)
            .annotate(
                total_tasks=task_stats,
                done_tasks=done_tasks
            )
        )

        # Configuramos el contexto para mostrar los projectos en que estamos colaborando
        context['collaborated_projects'] = (
            Project.objects
            .filter(collaborators=user)
            .exclude(owner=user)
            .annotate(
                total_tasks=task_stats,
                done_tasks=done_tasks
            )
        )
        
        return context

class ProjectDetailView(ProjectAccessMixin, DetailView):
    model = Project
    template_name = 'tasks/project_detail.html'
