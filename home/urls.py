from django.contrib import admin
from django.urls import path,include
from .views import IndexView,LoginView,LogoutView,SignupView,PasswordChangeView,DashboardView,FaviconView,UploadView,DonateView,APIView


urlpatterns = [
    path("",IndexView.as_view(),name="index"), # Landing page that user will see.
    path("login/",LoginView.as_view(),name="login"), # User can login here.
    path("logout/",LogoutView.as_view(),name="logout"), # User can login here.
    path("signup/",SignupView.as_view(),name="signup"), # User can signup here.
    path("upload/",UploadView.as_view(),name="upload"), # User can upload image here.
    path("donate/",DonateView.as_view(),name="donate"), # User can donate money here.
    path("change_password/",PasswordChangeView.as_view(),name="change_password"), # User can change their password here.
    path("dashboard/",DashboardView.as_view(),name="dashboard"), # Main Dashboard here.
    path("api/",APIView,name="api"), # API  here.
    path('favicon.ico', FaviconView),
]
