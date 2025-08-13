from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from .models import Employee
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def loginView(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        # Get username from email
        try:
            username = Employee.objects.get(email=email).user.username
        except Employee.DoesNotExist:
            return HttpResponse("Invalid username or password.")

        # Check if account is inactive
        if Employee.objects.get(email=email).status == "Inactive":
            return HttpResponse("Your account is inactive.")

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return HttpResponse("Invalid username or password.")

    return render(request, 'login.html')
