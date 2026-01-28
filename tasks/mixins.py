from django.core.exceptions import PermissionDenied
from django.views import View
from django.shortcuts import get_object_or_404

from .models import Project

# Cortesía de GPT este archivo.

class ProjectAccessMixin(View):
    """
    Permite acceso solo al owner o colaboradores.
    """

    def get_project(self):
        return get_object_or_404(Project, pk=self.kwargs['pk'])

    def dispatch(self, request, *args, **kwargs):
        project = self.get_project()
        user = request.user

        if project.owner != user and user not in project.collaborators.all():
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)
    
    
class ProjectOwnerRequiredMixin(ProjectAccessMixin):
    """
    Permite acceso solo al owner del proyecto.
    """

    def dispatch(self, request, *args, **kwargs):
        project = self.get_project()

        if project.owner != request.user:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)