from django import template
from django.core.urlresolvers import reverse


register = template.Library()

@register.tag
def selected(parser, token):
    """
    This template tag is useful for menus and navbars and such. It takes the
    same arguments as a standard django url tag, but outputs "selected" if
    the url is the current page. Outputs nothing otherwise.
    
    If you pass as a keyword argument exact=true, this will only output 
    "selected" if the user is on an exactly matching URL. By default, it will 
    output "selected" for anything at or beginning with the path.
    """
    bits = token.split_contents()
    if len(bits) < 2:
        raise template.TemplateSyntaxError("'%s' takes at least one argument"
            " (path to a view)" % bits[0])
    viewname = bits[1]
    args = []
    kwargs = {}
    if len(bits) > 2:
        bits = iter(bits[2:])
        for bit in bits:
            for arg in bit.split(","):
                if '=' in arg:
                    k, v = arg.split('=', 1)
                    k = k.strip()
                    kwargs[k] = parser.compile_filter(v)
                elif arg:
                    args.append(parser.compile_filter(arg))
    return SelectedNode(viewname, args, kwargs)

class SelectedNode(template.Node):
    def __init__(self, viewname, args, kwargs):
        self.viewname = viewname
        self.args = args
        self.kwargs = kwargs
        self.exact = kwargs.pop('exact', False)

    def render(self, context):
        args = [arg.resolve(context) for arg in self.args]
        kwargs = dict([(str(k), v.resolve(context))
            for k, v in self.kwargs.items()])
        url = reverse(self.viewname, args=args, kwargs=kwargs)
        request = context.get('request', None)
        if not request:
            raise ValueError('Must have request on the context.')
        if not self.exact and request.path.startswith(url):
            return u'selected'
        if self.exact:
            if '?' in request.path:
                path = request.path.split('?', 1)[0]
            else:
                path = request.path
            if path == url:
                return u'selected'
        return u''
