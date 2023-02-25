from django.contrib.admin.decorators import register
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Animal
from .forms import UserChangeForm,UserCreationForm,AnimalCreationForm
# Register your models here.
@register(User)
class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('email', 'name',)
    list_filter = ('is_verified', 'is_active')
    fieldsets = (
        ('User Data', {'fields': ('email', 'name', 'phone','is_verified')}),
        ('NGO Data', {'fields': ('latitude', 'longitude', 'active_members','tickets','address','website')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),  
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('id',)

@register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    add_form = AnimalCreationForm
    model = Animal
    list_display = ('id', 'status',)
    list_filter = ('status',)