from django.core.management.base import BaseCommand, CommandError
from monitor.models import Project


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        # parser.add_argument('id', nargs='+', type=int)
        return

    def handle(self, *args, **options):
        # self.stdout.write('Run the command with id {}'.format(options['id']))
        projects = Project.objects.all()
        for project in projects:
            self.stdout.write('project: {}'.format(project.name))
