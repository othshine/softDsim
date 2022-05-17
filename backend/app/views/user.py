import logging
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect


def register_request(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = UserCreationForm()
    return render(request=request, template_name="app/register.html", context={"form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                logging.info(f"Successful login user {username}.")
                return redirect("/")
            else:
                logging.error(f"Rejected login user {username}. Authentication failed.")
        else:
            logging.error(f"Invalid login form.")
    form = AuthenticationForm()
    return render(request=request, template_name="app/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    logging.info(f"Successful logout user {request.user.username}")
    return redirect('/')
