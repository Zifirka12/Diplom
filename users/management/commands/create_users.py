from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from users.models import User

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        admin_group, created = Group.objects.get_or_create(name='admin')
        teacher_group, created = Group.objects.get_or_create(name='teachers')
        student_group, created = Group.objects.get_or_create(name='students')

        admin_user = User.objects.create_user(
            username='Tengen',
            email='tengen@example.com',
            password='JUpass01',
            is_staff=True,
            is_superuser=True
        )
        admin_user.groups.add(admin_group)
        self.stdout.write(self.style.SUCCESS(f'Создан админ с именем: {admin_user.username}'))

        teacher_user = User.objects.create_user(
            username='Gojo',
            email='gojo@example.com',
            password='JUpass02'
        )
        teacher_user.groups.add(teacher_group)
        self.stdout.write(self.style.SUCCESS(f'Создан учитель с именем: {teacher_user.username}'))

        student_user = User.objects.create_user(
            username='Itadori',
            email='itadori@example.com',
            password='JUpass03'
        )
        student_user.groups.add(student_group)
        self.stdout.write(self.style.SUCCESS(f'Создан студент с именем: {student_user.username}'))
