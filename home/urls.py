from django.contrib import admin
from django.urls import path,include
from .views import IndexView,LoginView,LogoutView,SignupView,PasswordChangeView,DashboardView,FaviconView


urlpatterns = [
    path("",IndexView.as_view(),name="index"), # Landing page that user will see.
    path("login/",LoginView.as_view(),name="login"), # User can login here.
    path("logout/",LogoutView.as_view(),name="logout"), # User can login here.
    path("signup/",SignupView.as_view(),name="signup"), # User can signup here.
    path("change_password/",PasswordChangeView.as_view(),name="change_password"), # User can change their password here.
    path("dashboard/",DashboardView.as_view(),name="dashboard"), # Main Dashboard here.
    path('favicon.ico', FaviconView),
]
