from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Runs a script in the Django environment."
    args = '[script name]'

    def handle(self, *args, **options):
        if len(args) != 1:
            print 'You must specify one and only one script to run.'
            return
        script_name = args[0]

        try:
            scripts_root = __import__('scripts.%s' % script_name, globals(), locals(), [], -1)
            script = getattr(scripts_root, script_name)
        except ImportError:
            print 'Could not find the script "%s" under in the scripts directory.' % script_name
            return

        try:
            main = getattr(script, 'main')
        except AttributeError:
            print 'That script does not have a "main" function.'
            return

        main()
