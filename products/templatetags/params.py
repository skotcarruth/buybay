from django import template


register = template.Library()

def params(parser, token):
    """
    Creates a link to the current page, but with altered GET parameters.
    
    Usage::
    
        {% params [name]=[value] ... %}
    
    Name is the name of the GET parameter to set. Value can be a variable, 
    in which case its value is set as the parameter value. Or it can be a 
    quoted static value, in which case it is used (without the quotes). Or it 
    can be two such values, comma-separated, and it will toggle between them
    (choosing the first value if not yet set).
    """
    bits = token.split_contents()
    if len(bits) < 2:
        raise template.TemplateSyntaxError('%r tag requires at least one argument.' % bits[0])
    params = {}
    for bit in bits[1:]:
        if not '=' in bit:
            raise tempalte.TemplateSyntaxError('%r tag arguments must be in the form "[name]=[value]".' % bits[0])
        name, value = bit.split('=', 1)
        if ',' in value:
            val1, val2 = value.split(',', 1)
            value = (val1, val2)
        params[name] = value
    return ParamsNode(params)

class ParamsNode(template.Node):
    def __init__(self, params):
        self.params = params

    def resolve_value(self, value, context):
        if value[0] == value[-1] and value[0] in ('\'', '"'):
            return value[1:-1]
        try:
            return template.Variable(value).resolve(context)
        except template.VariableDoesNotExist:
            return ''

    def render(self, context):
        request_params = context['request'].GET.copy()
        reset_toggles = False
        toggles = []
        for name, value in self.params.iteritems():
            if isinstance(value, tuple):
                toggles.append(name)
            else:
                set_value = self.resolve_value(value, context)
                if request_params.get(name, None) != set_value:
                    reset_toggles = True
                request_params[name] = set_value
        for name in toggles:
            val1, val2 = self.params[name]
            val1 = self.resolve_value(val1, context)
            if reset_toggles:
                set_value = val1
            else:
                val2 = self.resolve_value(val2, context)
                current = request_params.get(name, None)
                if current == val1:
                    set_value = val2
                else:
                    set_value = val1
            request_params[name] = set_value
        return '?%s' % request_params.urlencode()

register.tag('params', params)
