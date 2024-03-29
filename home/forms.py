from django.contrib.auth.forms import UserCreationForm, UserChangeForm,AuthenticationForm,PasswordChangeForm
from .models import User,Animal
from django import forms

# Signup Form. Visible at /signup
class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('email','name','phone','verification_file','about','active_members','address','website')

#Only for admin page. Site uses api
class AnimalCreationForm(forms.Form):
    class Meta:
        model = Animal
        fields = ('image',"latitude","longitude","status")

# Change user password without old password. Don't use this.
class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email','name')

# Login the user. Visible at /login
class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('email','password')

# Change user password with old password.
class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="",widget=forms.PasswordInput(attrs={'placeholder': 'Old Password'}))
    new_password1 = forms.CharField(label="",widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}))
    new_password2 = forms.CharField(label="",widget=forms.PasswordInput(attrs={'placeholder': 'New Password Confirmation'}))
    
    class Meta:
        model = User