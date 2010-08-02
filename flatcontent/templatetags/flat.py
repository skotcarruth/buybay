from django import template
from django.contrib.markup.templatetags import markup

from buybay.flatcontent.models import Blurb


register = template.Library()

def blurb(parser, token):
    """
    Inserts the contents of a flatcontent blurb into the page. 
    
    Usage::
    
        {% blurb [slug] %}

    """
    bits = token.split_contents()
    if len(bits) != 2:
        raise template.TemplateSyntaxError('%r tag requires exactly one argument.' % bits[0])
    return BlurbNode(bits[1])

class BlurbNode(template.Node):
    def __init__(self, slug):
        self.slug = slug

    def render(self, context):
        if self.slug[0] in ('\'', '"') and self.slug[0] == self.slug[-1]:
            blurb_slug = self.slug[1:-1]
        else:
            try:
                blurb_slug = template.Variable(self.slug).resolve(context)
            except template.VariableDoesNotExist:
                return u''
        try:
            blurb = Blurb.objects.get(is_active=True, slug=blurb_slug)
        except Blurb.DoesNotExist:
            return u''
        return markup.textile(blurb.content)

register.tag('blurb', blurb)
