from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
import re

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = '__all__'
        # exclude = ['user']
        widgets = {'user': forms.HiddenInput()}

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean(self):
        cleaned_data = super(CreateUserForm, self).clean()
        password1 = cleaned_data.get('password1')
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$"
        pat = re.compile(reg)
        mat = re.search(pat, password1)
        if not mat:
            raise forms.ValidationError("Password should have number, uppercase, lowercase, special symbol and from 8 chacracters long")
        return cleaned_data