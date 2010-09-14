from datetime import datetime, date, time
from decimal import Decimal
from functools import wraps
import json

from django.db import models
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from features.models import Feature


def _json_prep(data):
    """Recursively converts values to JSON-serializable alternatives."""
    if isinstance(data, (list, tuple, set, frozenset)):
        return [_json_prep(item) for item in data]
    if isinstance(data, dict):
        return dict([(str(key), _json_prep(value)) for key, value in data.iteritems()])
    if isinstance(data, basestring):
        return str(data)
    if isinstance(data, Decimal):
        return float(data)
    if isinstance(data, (date, time, datetime)):
        return str(data)
    if isinstance(data, models.Model):
        return None
    return data

def json_response(view):
    """
    The view function should return a normal Python object (JSON-serializable,
    please). The wrapper will then convert this to JSON and return an
    appropriate HttpResponse object.
    """
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        data = view(request, *args, **kwargs)
        return HttpResponse(json.dumps(_json_prep(data)), mimetype='application/javascript')
    return wrapper

def index(request):
    """The homepage."""
    features = Feature.objects.filter(is_active=True).all()
    return render_to_response('index.html', {
        'features': features,
    }, context_instance=RequestContext(request))
