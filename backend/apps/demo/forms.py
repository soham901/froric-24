from django import forms
from .models import Item
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class BraintreePaymentForm(forms.Form):
    payment_method_nonce = forms.CharField(widget=forms.HiddenInput)


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))