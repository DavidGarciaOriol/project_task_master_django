from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count, Q
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView
from django.urls import reverse
from django.views.generic import UpdateView

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
        project = self.get_object()
        
        tasks = project.tasks.order_by("title") # type: ignore

        context["tasks"] = tasks

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
        
### CRUD VIEWS ###
       
class TaskCreateView(ProjectAccessMixin, CreateView):
    model = Task
    fields = ["title", "description", "status"]

    def form_valid(self, form):
        project = Project.objects.get(pk=self.kwargs["project_pk"])
        form.instance.project = project
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("tasks:project_detail", args=[self.object.project.pk]) # type: ignore

class TaskUpdateView(ProjectAccessMixin, UpdateView):
    model = Task
    fields = ["title", "description", "status"]

    def get_success_url(self):
        return reverse("tasks:project_detail", args=[self.object.project.pk]) # type: ignore
    
def toggle_task_status(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if task.status == Task.Status.DONE:
        task.status = Task.Status.IN_PROGRESS
    else:
        task.status = Task.Status.DONE

    task.save()
    return redirect("tasks:project_detail", task.project.pk)