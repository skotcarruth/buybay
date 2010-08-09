from datetime import timedelta
from django.core.urlresolvers import resolve
from blog.models import Post, Tag


def archive(request):
    """Adds a list of months in the blog archive."""
    # Don't waste the DB hits if it's not a blog page
    view, args, kwargs = resolve(request.path)
    if view.__module__ != 'blog.views':
        return {}

    # Collect the list of months and number of blog posts each
    start_date = Post.objects.active().order_by('pub_date')[0]\
        .pub_date.date().replace(day=1)
    end_date = Post.objects.active().order_by('-pub_date')[0]\
        .pub_date.date().replace(day=1)
    months = []
    while start_date <= end_date:
        num_posts = Post.objects.active().filter(
            pub_date__year=start_date.year,
            pub_date__month=start_date.month,
        ).count()
        months.append((start_date, num_posts))
        start_date = (start_date + timedelta(days=31)).replace(day=1)
    return {'archive_months': months}

def tags(request):
    """Adds a list of product tags to the context."""
    # Don't waste the DB hits if it's not a products page
    view, args, kwargs = resolve(request.path)
    if view.__module__ != 'blog.views':
        return {}

    # Return the list of active tags
    return {'blog_tags': Tag.objects.active()}
