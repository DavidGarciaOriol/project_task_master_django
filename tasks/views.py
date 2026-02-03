from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count, Q
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.urls import reverse
from django.shortcuts import get_object_or_404

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object

        total_tasks = project.tasks.count()
        done_tasks = project.tasks.filter(
            status=Task.Status.DONE
        ).count()

        context['total_tasks'] = total_tasks
        context['done_tasks'] = done_tasks
        context['pending_tasks'] = total_tasks - done_tasks

        return context

class TaskStatusUpdateView(ProjectAccessMixin, UpdateView):
    model = Task
    fields = ['status']
    template_name = 'tasks/task_status_form.html'

    def get_object(self, queryset=None):
        task = get_object_or_404(Task, pk=self.kwargs['pk'])
        self.project = task.project
        self.kwargs['pk'] = self.project.pk
        return task

    def get_success_url(self):
        return reverse(
            'tasks:project_detail',
            args=[self.project.pk]
        )
