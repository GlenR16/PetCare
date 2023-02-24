from django.contrib.auth.forms import UserCreationForm, UserChangeForm,AuthenticationForm,PasswordChangeForm
from .models import User,Animal
from django.forms import Form

# Signup Form. Visible at /signup
class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('email','name')

#Only for admin page. Site uses api
class AnimalCreationForm(Form):
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
    class Meta:
        model = User