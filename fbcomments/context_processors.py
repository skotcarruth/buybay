from django.conf import settings


def settings_context(request):
    """Adds the settings object to the context."""
    return {'settings': settings}
