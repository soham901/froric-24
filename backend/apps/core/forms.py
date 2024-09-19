from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from .models import Crew, Expense
from django.core.validators import MaxValueValidator, MinValueValidator


class JoinCrewForm(forms.Form):
    crew_name = forms.CharField(max_length=100, label='Crew Name')
    joining_code = forms.CharField(max_length=20, label='Joining Code')


class CrewForm(forms.ModelForm):
    class Meta:
        model = Crew
        fields = ['name', 'description', 'joining_code']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'joining_code': forms.TextInput(attrs={'placeholder': 'Optional: Set a code for others to join'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('name', css_class='mb-3'),
            Field('description', css_class='mb-3'),
            Field('joining_code', css_class='mb-3'),
            Submit('submit', 'Create Crew', css_class='btn btn-primary')
        )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Crew.objects.filter(name=name).exists():
            raise ValidationError("A crew with this name already exists.")
        return name


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['name', 'total_amount', 'date', 'description', 'category']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'category': forms.Select(choices=Expense.CATEGORY_CHOICES, attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('name', css_class='mb-3'),
            Field('total_amount', css_class='mb-3'),
            Field('date', css_class='mb-3'),
            Field('description', css_class='mb-3'),
            Field('category', css_class='mb-3'),
            Submit('submit', 'Create Expense', css_class='btn btn-primary')
        )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Expense.objects.filter(name=name).exists():
            raise ValidationError("An expense with this name already exists.")
        return name



class ContributionForm(forms.Form):
    amount = forms.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(0.01)])

    def __init__(self, *args, **kwargs):
        self.expense = kwargs.pop('expense', None)
        super().__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount > self.expense.total_amount:
            raise ValidationError("The contribution amount cannot exceed the total expense amount.")
        return amount
