from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from .form import RegisterUser
# Create your views here.
def home(request):
    return render(request, 'index.html')
def register_view(request):
    if request.method == "POST":
        form = RegisterUser(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            user = form.save(commit=False)
            user.is_superuser = False
            user.is_staff = False
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login_view')
    else:
        form = RegisterUser()
    return render(request, "user/register.html", {'form':form})
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/")
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})

