from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from artists.models import Artist


def index(request):
    """List of all artists."""
    artists = Artist.objects.filter(is_active=True).all()
    return render_to_response('artists/index.html', {
        'artists': artists,
    }, context_instance=RequestContext(request))

def artist(request, artist_slug=None):
    """Detail page for an artist."""
    artist = get_object_or_404(Artist, is_active=True, slug=artist_slug)
    artist_list = Artist.objects.filter(is_active=True).all()
    return render_to_response('artists/artist.html', {
        'artist': artist,
        'artist_list': artist_list,
    }, context_instance=RequestContext(request))
