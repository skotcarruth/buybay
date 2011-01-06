from django.db import models


class IPNRecord(models.Model):
    """A record of every successful IPN call from PayPal to avoid duplicates."""
    transaction_id = models.CharField(max_length=30, unique=True)
    data = models.TextField()
    created_ts = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_ts',)

    def __unicode__(self):
        return 'IPN %s' % self.transaction_id
