from datetime import datetime

from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from blog.models import Post, Tag


def index(request):
    """The news landing page."""
    pass

def archive_year(request, year=None):
    """Archive for a particular year."""
    pass

def archive_month(request, year=None, month=None):
    """Archive for a particular month."""
    pass

def archive_day(request, year=None, month=None, day=None):
    """Archive for a particular day."""
    pass

def post(request, year=None, month=None, day=None, slug=None):
    """A blog post."""
    try:
        month = datetime.strptime(month, '%b').month
    except ValueError:
        raise Http404
    post = get_object_or_404(Post, status=Post.LIVE, slug=slug,
        pub_date__year=year, pub_date__month=month, pub_date__day=day)
    return render_to_response('blog/post.html', {
        'post': post,
    }, context_instance=RequestContext(request))

def tag(request, tag_slug=None):
    """Lists the blog entries in this category."""
    pass
