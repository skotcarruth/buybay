import re

from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from sorl.thumbnail.main import DjangoThumbnail


class AdminImageWidget(forms.FileInput):
    """
    Like the django.contrib.admin.widgets.AdminFileWidget, but with an image 
    preview.
    """
    link_re = re.compile(r'<a target="_blank" href="([^"]*)">([^<]*)</a>')
    thumb_size = (60, 45)
    opts = {'crop': None, 'upscale': None}

    def __init__(self, attrs={}):
        super(AdminImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, 'url'):
            thumbnail = DjangoThumbnail(value, self.thumb_size,
                opts=self.opts, quality=85)
            output.append('<img src="%s" style="margin:0 10px" /> %s ' %
                (unicode(thumbnail), _('Change:')))
        output.append(super(AdminImageWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))
