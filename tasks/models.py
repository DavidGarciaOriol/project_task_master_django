from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Project(models.Model):

    title = models.CharField(max_length = 200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    deadline = models.DateField()

    # Propietario de la tarea
    owner = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = 'owned_projects'
    )

    # Colaboradores de la tarea
    collaborators = models.ManyToManyField(
        User,
        related_name="collaborated_projects",
        blank=True
    )

    def clean(self):
        """
        Valida no introducir una fecha límite inferior a la actual.
        """
        if self.deadline < timezone.now().date():
            raise ValidationError(
                {'deadline': 'La fecha límite no puede estar en el pasado.'}
            )
        
    def __str__(self) -> str:
        return self.title
    
class Task(models.Model):

    # Clase del Status de la tarea
    class Status(models.TextChoices):

        TODO = 'TODO', 'Pendiente'
        IN_PROGRESS = 'INPROG', 'En progreso'
        DONE = 'DONE', 'Completada'

    # Clase de la prioridad de la tarea
    class Priority(models.TextChoices):
        LOW = 'L', 'Baja'
        MEDIUM = 'M', 'Media'
        HIGH = 'H', 'Alta'

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # Estatus por defecto de la tarea
    status = models.CharField(
        max_length=6,
        choices=Status.choices,
        default=Status.TODO
    )

    # Ref. Projecto al que pertenece la tarea
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    # Prioridad por defecto de la tarea
    priority = models.CharField(
        max_length=1,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )

    # Asignación de la tarea
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks'
    )

    def __str__(self):
        return f'{self.title} ({self.project.title})'

