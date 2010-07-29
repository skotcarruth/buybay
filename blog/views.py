from datetime import datetime

from django.core import paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from blog.models import Post, Tag


PER_PAGE = 10

class Paginator(paginator.Paginator):
    def __init__(self, request, object_list, **kwargs):
        self.request = request
        super(Paginator, self).__init__(object_list, PER_PAGE, **kwargs)

    def request_page(self):
        try:
            page_num = int(self.request.GET.get('page', 1))
        except ValueError:
            page_num = 1
        try:
            page = self.page(page_num)
        except (paginator.EmptyPage, paginator.InvalidPage):
            page = self.page(1)
        return page

def index(request):
    """The news landing page."""
    posts = Post.objects.active()
    page = Paginator(request, posts).request_page()
    return render_to_response('blog/index.html', {
        'page': page,
    }, context_instance=RequestContext(request))

def archive_month(request, year=None, month=None):
    """Archive for a particular month."""
    try:
        month = datetime.strptime(month, '%b').month
    except ValueError:
        raise Http404
    month = datetime(int(year), month, 1)
    posts = Post.objects.active().filter(pub_date__year=month.year, pub_date__month=month.month)
    page = Paginator(request, posts).request_page()
    return render_to_response('blog/archive_month.html', {
        'month': month,
        'page': page,
    }, context_instance=RequestContext(request))

def post(request, year=None, month=None, day=None, slug=None):
    """A blog post."""
    try:
        month = datetime.strptime(month, '%b').month
    except ValueError:
        raise Http404
    post = get_object_or_404(Post.objects.active(), slug=slug,
        pub_date__year=year, pub_date__month=month, pub_date__day=day)
    return render_to_response('blog/post.html', {
        'post': post,
    }, context_instance=RequestContext(request))

def tag(request, tag_slug=None):
    """Lists the blog entries in this category."""
    tag = get_object_or_404(Tag.objects.active(), slug=tag_slug)
    posts = tag.post_set.active()
    page = Paginator(request, posts).request_page()
    return render_to_response('blog/tag.html', {
        'tag': tag,
        'page': page,
    }, context_instance=RequestContext(request))
