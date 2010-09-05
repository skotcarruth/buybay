from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from flatcontent.models import Page


def index(request):
    """Exists only for reversing its url for the selected template tag."""
    raise Http404

def page(request, page_slug=None):
    """Displays a flat page."""
    page = get_object_or_404(Page, is_active=True, slug=page_slug)
    return render_to_response('flatcontent/page.html', {
        'page': page,
    }, context_instance=RequestContext(request))
