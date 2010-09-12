import asyncore
import smtpd

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Starts a development mail server that prints mail sent via localhost:port to stdout."

    def handle(self, *args, **options):
        smtpd.DebuggingServer(('localhost', settings.EMAIL_PORT), ('localhost', 25))
        print 'smptd started on localhost.'
        try:
            asyncore.loop()
        except KeyboardInterrupt:
            pass
