from django.core.exceptions import PermissionDenied
from django.views import View
from django.shortcuts import get_object_or_404

from .models import Project

# Cortesía de GPT este archivo.

class ProjectAccessMixin:
    """
    Permite acceso solo al owner o colaboradores del proyecto.
    Funciona tanto con pk como con project_pk.
    """

    def get_project(self): 
        if hasattr(self, "object") and self.object: # type: ignore
            # Caso DetailView / UpdateView
            if hasattr(self.object, "project"):# type: ignore
                return self.object.project# type: ignore
            return self.object# type: ignore

        if "project_pk" in self.kwargs:# type: ignore
            return get_object_or_404(Project, pk=self.kwargs["project_pk"])# type: ignore

        if "pk" in self.kwargs:# type: ignore
            return get_object_or_404(Project, pk=self.kwargs["pk"])# type: ignore

        raise AttributeError("No se pudo determinar el proyecto")

    def dispatch(self, request, *args, **kwargs):
        project = self.get_project()
        user = request.user

        if project.owner != user and user not in project.collaborators.all():
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)# type: ignore
    
    
class ProjectOwnerRequiredMixin(ProjectAccessMixin):
    """
    Permite acceso solo al owner del proyecto.
    """

    def dispatch(self, request, *args, **kwargs):
        project = self.get_project()

        if project.owner != request.user:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)