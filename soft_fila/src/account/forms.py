from datetime import datetime
from django import forms
from django.core.validators import validate_email
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UserChangeForm
from django.core.exceptions import ValidationError
from .models import FilaUser,Profile#,FilaSub

class RegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True,validators=[validate_email],widget=forms.EmailInput(attrs={'placeholder':'Enter your email'}))
    email2 = forms.EmailField(required=True,validators=[validate_email],widget=forms.EmailInput(attrs={'placeholder':'Enter your email'}))

    class Meta:

        model = FilaUser
        fields = (
            'first_name',
            'last_name',
            'email',
            'email2',
            'password1',
            'password2',
        )
        exclude = ('password1','password2')

    def clean_email(self):

        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')

        if email and email2 and email!=email2:
            raise ValueError("emails dont match")

        return email

    def clean_password(self):

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1!=password2:
            raise ValidationError("passwords dont match")

        return password1

    def save(self,commit = True):

        user = super().save(commit=False)

        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')

        user.first_name = first_name
        user.last_name = last_name

        user.email = self.cleaned_data.get('email')
        user.set_password(self.cleaned_data.get('password1'))

        if commit:
            user.save()

        return user

class EditProfileForm(UserChangeForm):

    class Meta:

        model = Profile
        fields = '__all__'

class CustomProfileForm(forms.ModelForm):

    #email = forms.EmailField(required=True,validators=[validate_email],widget=forms.EmailInput())
    class Meta:

        model = Profile

        fields = [
            'first_name',
            'last_name',
            'photo',
            'phone',
            'instagram',
            'facebook',
            'caption',
        ]
        exclude = ['password']

    def save(self, commit=True):

        user = super().save(commit=False)

        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.photo = self.cleaned_data.get('photo')
        user.phone_number = self.cleaned_data.get('phone')
        user.instagram = self.cleaned_data.get('instagram')
        user.facebook = self.cleaned_data.get('facebook')
        user.caption = self.cleaned_data.get('caption')

        if commit:
            user.save()

        return user

class CustomAuthForm(AuthenticationForm):

    remember_me = forms.BooleanField(label='remember me',required=False,widget=forms.CheckboxInput())

    def clean(self):

        super().clean()

        remember = self.cleaned_data.get('remember_me')

        if not remember:
            self.request.session.set_expiry(0)

        return remember
