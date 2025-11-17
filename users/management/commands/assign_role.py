"""
Management command to assign roles to users
Usage: python manage.py assign_role <email> <role>
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Assign a role to a user'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='User email address')
        parser.add_argument('role', type=str, help='Role to assign (admin, agent, client, developer, investor)')

    def handle(self, *args, **options):
        email = options['email']
        role = options['role']

        # Validate role
        valid_roles = ['admin', 'agent', 'client', 'developer', 'investor']
        if role not in valid_roles:
            self.stdout.write(self.style.ERROR(f'Invalid role: {role}'))
            self.stdout.write(self.style.WARNING(f'Valid roles: {", ".join(valid_roles)}'))
            return

        # Get user
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User not found: {email}'))
            return

        # Assign role
        old_role = user.role
        user.role = role
        user.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully assigned role "{role}" to {email}'))
        self.stdout.write(self.style.SUCCESS(f'Previous role: {old_role}'))

