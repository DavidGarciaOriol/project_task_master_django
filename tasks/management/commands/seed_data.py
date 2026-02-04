from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
import random

from datetime import timedelta
from django.utils import timezone

from tasks.models import Project, Task

User = get_user_model()

class Command(BaseCommand):
    help = "Prueba la base de datos con Fake"
    
    def handle(self, *args, **options):
        fake = Faker("es_ES")
        
        self.stdout.write(self.style.SUCCESS("Iniciando poblado de datos..."))
        
        self.create_users(fake)
        self.create_projects(fake)
        self.create_tasks(fake)
        
        self.stdout.write(self.style.SUCCESS("Poblado finalizado"))
    
    def create_users(self, fake, total=10):
        users = []

        for i in range(total):
            username = fake.user_name() + str(i)
            email = fake.email()

            user = User.objects.create_user(
                username=username,
                email=email,
                password="password123"
            )
            users.append(user)

        self.stdout.write(self.style.SUCCESS(f"{total} usuarios creados"))

        
    def create_projects(self, fake, total=5):
        users = list(User.objects.all())

        for _ in range(total):
            owner = random.choice(users)

            project = Project.objects.create(
                title=fake.sentence(nb_words=3),
                description=fake.paragraph(),
                owner=owner,
                deadline=timezone.now().date() + timedelta(
                    days=random.randint(7, 90)
                )
            )

            collaborators = random.sample(
                users,
                k=random.randint(0, min(3, len(users)))
            )

            project.collaborators.set(collaborators)

        self.stdout.write(self.style.SUCCESS(f"{total} proyectos creados"))
            
    def create_tasks(self, fake, total_per_project=10):
        projects = Project.objects.all()

        for project in projects:
            for _ in range(total_per_project):
                Task.objects.create(
                    title=fake.sentence(nb_words=4),
                    description=fake.paragraph(),
                    project=project,
                    status=random.choice(Task.Status.values)
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Tareas creadas ({total_per_project} por proyecto)"
            )
        )
