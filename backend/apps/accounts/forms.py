from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, HTML
from django import forms


User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'password1',
            'password2',
            Submit('submit', 'Sign Up', css_class='btn btn-primary w-100 mt-3')
        )


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            Div(
                'password',
                # HTML("""
                #     <button type="button" class="btn btn-outline-secondary toggle-password" data-target="id_password">
                #         <i class="fa fa-eye"></i>
                #     </button>
                # """),
                css_class='password-wrapper'
            ),
            Submit('submit', 'Log In', css_class='btn btn-primary w-100 mt-3')
        )

    class Media:
        css = {
            'all': ('css/custom_form.css',)
        }
        js = ('js/toggle_password.js',)


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save Changes', css_class='btn btn-primary w-100 mt-3')
        )
