from django import forms

from orders.models import Order


class OrderForm(forms.ModelForm):
    """Form for entering an extra donation amount and order notes."""
    DONATION_AMOUNTS = (
        ('0', '$0'),
        ('10', '$10'),
        ('50', '$50'),
        ('100', '$100'),
        ('500', '$500'),
    )
    donation = forms.TypedChoiceField(choices=DONATION_AMOUNTS, coerce=int, initial=0)
    notes = forms.CharField(required=False, label='Notes:', widget=forms.Textarea)

    class Meta:
        model = Order
        fields = ('donation', 'notes',)
