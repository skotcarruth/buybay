from django import forms

from products.models import ProductComment


class CommentForm(forms.ModelForm):
    """Form for adding a comment on a product."""
    class Meta:
        model = ProductComment
        exclude = ('product', 'is_active',)
        widgets = {
            'facebook_id': forms.HiddenInput(),
            'name': forms.HiddenInput(),
            'thumb_url': forms.HiddenInput(),
        }
