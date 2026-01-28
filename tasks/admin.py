from django.contrib import admin
from .models import Project, Task

# Cortesía de GPT: creamos un registro para los modelos.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'deadline', 'created_at')
    list_filter = ('deadline', 'owner')
    search_fields = ('title', 'description')
    filter_horizontal = ('collaborators',)
    ordering = ('-created_at',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'priority', 'assigned_to')
    list_filter = ('status', 'priority', 'project')
    search_fields = ('title', 'description')
    ordering = ('project', 'priority')
