from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView,RedirectView
from .forms import UserCreationForm,UserLoginForm,PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.auth import login,logout,authenticate,update_session_auth_hash
from .models import Animal,Message

from .models import STATUS

FaviconView = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

class IndexView(TemplateView):
    template_name = "index.html"

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name","")
        email = request.POST.get("email","")
        message = request.POST.get("message","")
        if name != "" and email != "" and message != "":
            message = Message(name=name,email=email,message=message)
            message.save()
            return self.render_to_response({"submitted":True})
        return self.render_to_response({"submitted":False})

class DonateView(TemplateView):
    template_name = "donate.html"

class LogoutView(RedirectView):
    permanent = True
    pattern_name = 'login'

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super().get_redirect_url(*args, **kwargs)

class UploadView(TemplateView):
    template_name = "upload.html"

    def post(self, request, *args, **kwargs):
        image = request.FILES['image']
        latitude = request.POST.get("latitude","")
        longitude = request.POST.get("longitude","")
        if image != "" and latitude != "" and longitude != "":
            animal = Animal(image=image,latitude=latitude,longitude=longitude)
            animal.save()
        else:
            return JsonResponse(data={"submitted":False})
        return JsonResponse(data={"submitted":True})
        
class LoginView(TemplateView):
    template_name = "authentication/login.html"

    def post(self, request, *args, **kwargs):
            form = UserLoginForm(data=request.POST)
            if form.is_valid():
                user = authenticate(request,email=request.POST.get("username",""),password=request.POST.get("password",""))
                login(request,user)
                return redirect("/dashboard")
            else:
                return self.render_to_response({"form":form})

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/dashboard/")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = UserLoginForm()
        return context

class SignupView(TemplateView):
    template_name = "authentication/signup.html"

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect("/dashboard")
        else:
            return self.render_to_response({"form":form})

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/dashboard/")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = UserCreationForm()
        return context

class PasswordChangeView(TemplateView):
    template_name = "authentication/passwordchange.html"

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            return render(request,"authentication/passworddone.html")
        else:
            return self.render_to_response({"form":form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PasswordChangeForm(self.request.user)
        return context

class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = "dashboard.html"

    login_url = '/login'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
