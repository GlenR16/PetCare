from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView,RedirectView
from .forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate,update_session_auth_hash
from .models import Animal,Message,User
from django.contrib.auth.hashers import make_password
from .models import STATUS
from django.shortcuts import get_object_or_404
from .serializers import AnimalSerializer
SEARCH_RADIUS = 5000

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
            email = request.POST.get("email","")
            password = request.POST.get("password","")
            if email != "" and password != "":
                user = authenticate(request,email=email,password=password)
                if user != None:
                    login(request,user)
                    return redirect("/dashboard")
            return self.render_to_response({"error":True})

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/dashboard/")
        return super().get(request, *args, **kwargs)

class SignupView(TemplateView):
    template_name = "authentication/signup.html"

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name","")
        email = request.POST.get("email","")
        phone = request.POST.get("phone","")
        about = request.POST.get("about","")
        password1 = request.POST.get("password1","")
        password2 = request.POST.get("password2","")
        website = request.POST.get("website","")
        address = request.POST.get("address","")
        city = request.POST.get("city","")
        state = request.POST.get("state","")
        postalcode = request.POST.get("postalcode","")
        activemembers = request.POST.get("activemembers","")
        alerts = request.POST.get("alerts","")
        country = request.POST.get("country","")
        candidates = request.POST.get("candidates","")
        verificationfile = request.FILES["verificationfile"]
        if name != "" and verificationfile != "" and email != "" and phone != "" and about != "" and password1 != "" and password2 != "" and website != "" and address != "" and city != "" and state != "" and postalcode != "" and alerts != "" and country != "" and candidates != "" and password1 != "" and password1 == password2:
            address = address +", "+ city +" "+ postalcode+", " + state +", "+ country
            user = User(name=name,email=email,phone=phone,verification_file=verificationfile,about=about,active_members=activemembers,website=website,address=address)
            user.set_password(password1)
            user.save()
            login(request,user)
            return redirect("/dashboard")
        else:
            return self.render_to_response({"error":True})

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/dashboard/")
        return super().get(request, *args, **kwargs)

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

    def post(self, request, *args, **kwargs):
        ticket_id = request.POST.get("id","")
        status = request.POST.get("status","")
        if ticket_id != "" and status != "":
            animal = get_object_or_404(Animal,pk=ticket_id)
            if animal.status == "Allotted" and animal in request.user.ticket:
                animal.status = STATUS[status]
                animal.save()
                return self.render_to_response({"submitted":True})
        return self.render_to_response({"submitted":False})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tickets"] = self.request.user.tickets.all()
        return context

@login_required(login_url='/login/')
def APIView(request):
    offset_lat = 360 * SEARCH_RADIUS / 40075016.686
    offset_long = 360 * SEARCH_RADIUS / 40075017
    up = request.user.latitude + offset_lat
    down = request.user.latitude - offset_lat
    left = request.user.longitude - offset_long
    right = request.user.longitude + offset_long
    valid = Animal.objects.filter(latitude__lte=up,latitude__gte=down,longitude__lte=right,longitude__gte=left,status="Pending")
    if request.method == "POST":
        id = request.POST.get("id",None)
        animal = get_object_or_404(valid,pk=id)
        user = User.objects.get(pk=request.user.id)
        animal.status = STATUS["ALLOTTED"]
        animal.save()
        user.tickets.add(animal)
        return JsonResponse(data={"submitted":True})
    data = AnimalSerializer(valid,many=True)
    return JsonResponse(data=data.data,safe=False)