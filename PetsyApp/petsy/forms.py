from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from petsy.models import UserPetsy


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = UserPetsy
        fields = ('email',
                  'username',
                  'password',
                  'password2')



