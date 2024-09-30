from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
  email = forms.EmailField(label="Email Address", required=True)
  password = forms.CharField(label="Password", widget=forms.PasswordInput)
  confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

  class Meta:
    model = User
    fields = ('username', 'email', 'password')

  def clean(self):
    cleaned_data = super(RegisterForm, self).clean()
    password = cleaned_data.get('password')
    confirm_password = cleaned_data.get('confirm_password')
    if password != confirm_password:
      raise forms.ValidationError("Passwords don't match")
    return cleaned_data