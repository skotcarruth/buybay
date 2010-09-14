from datetime import datetime, timedelta
import smtplib
import socket

from django.core.mail import EmailMultiAlternatives
from django.db import models


RETRY_DELAY_MINUTES = 60
RETRY_DELAY = timedelta(minutes=RETRY_DELAY_MINUTES)

class MessageManager(models.Manager):
    """Manager for the Message model."""
    def to_be_sent(self):
        q = self
        q = q.filter(sent=False)
        q = q.filter(scheduled_delivery__lte=datetime.utcnow())
        q = q.filter(failed_send_attempts__lt=models.F('max_send_attempts'))
        return q

class Message(models.Model):
    """An email message to be sent."""
    to_email = models.CharField(max_length=256)
    from_email = models.CharField(max_length=256)
    subject = models.CharField(max_length=256)
    body_text = models.TextField()
    body_html = models.TextField('body HTML', blank=True)

    scheduled_delivery = models.DateTimeField(default=datetime.utcnow)
    sent = models.BooleanField(default=False)
    sent_ts = models.DateTimeField(null=True, blank=True)
    failed_send_attempts = models.PositiveIntegerField(default=0)
    max_send_attempts = models.PositiveIntegerField(default=3)

    created_ts = models.DateTimeField(auto_now_add=True)
    logs = models.TextField(blank=True)

    objects = MessageManager()

    class Meta:
        ordering = ['-scheduled_delivery']

    def __unicode__(self):
        return '%s - %s' % (self.to_email, self.subject)

    def add_log(self, message):
        """Adds a line to the message logs."""
        self.logs += '%s UTC - %s\n' % (
            datetime.utcnow().strftime('%Y-%m-%d %H:%M'),
            message,
        )

    def should_retry(self):
        """Determines whether, if sending fails, it should be retried."""
        return self.failed_send_attempts < self.max_send_attempts

    def send(self):
        """Attempts to send the email."""
        # Construct the message object
        message = EmailMultiAlternatives(
            self.subject, self.body_text, self.from_email, [self.to_email])
        if self.body_html:
            message.attach_alternative(self.body_html, 'text/html')

        # Attempt to send the message, and log the outcome
        try:
            message.send()
        except (smtplib.SMTPException, socket.error) as e:
            self.failed_send_attempts += 1
            if self.should_retry():
                self.scheduled_delivery = datetime.utcnow() + RETRY_DELAY
                self.add_log('WARNING: Problem sending the email. Will retry '
                    'in %d minutes. (%s)' % (RETRY_DELAY_MINUTES, e))
            else:
                self.add_log('ERROR: Problem sending the email. Maximum '
                    'number of retries reached. Message will not be sent. '
                    '(%s)' % e)
        else:
            self.sent = True
            self.sent_ts = datetime.utcnow()
            self.add_log('SUCCESS: Message sent successfully.')
        self.save()
        return self.sent

