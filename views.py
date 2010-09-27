from django.shortcuts import render_to_response
from django.template import RequestContext

from features.models import Feature


def index(request):
    """The homepage."""
    features = Feature.objects.filter(is_active=True).all()
    return render_to_response('index.html', {
        'features': features,
    }, context_instance=RequestContext(request))
