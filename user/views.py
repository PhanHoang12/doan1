from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from .form import RegisterUser, UpdateUserForm
from django.contrib.auth.decorators import login_required
from country.models import Country,CustomUser
from product.models import Product
import json
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages



# Create your views here.
def home(request):
    # return render(request, 'index.html')
    products = Product.objects.all().order_by('-created_at')[:6]
    for product in products:
        if product.images:
            product.image_filenames = json.loads(product.images)
        else:
            product.image_filenames = []
    return render(request, "index.html", {"products": products})
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
            print(request.user)
            return redirect("/")
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})
def custom_logout(request):
    logout(request)
    return redirect('login_view')
@login_required
def account_update(request):
    user = request.user
    # countries = Country.objects.all()
    # if request.method == "POST":
    #     user.username = request.POST.get("username")
    #     user.email = request.POST.get("email")
    #     user.first_name = request.POST.get("first_name")
    #     user.last_name = request.POST.get("last_name")
    #     country_id = request.POST.get("id_country")
    #     if country_id:
    #         user.id_country_id = country_id
    #     else:
    #         user.id_country = None
    #     if request.FILE.get("avatar"):
    #         user.avatar = request.FILE.get("avatar")
    #     password = request.POST.get("password")
    #     if password:
    #         user.set_password(password)
    #     user.save()
    #     return  redirect('account_update')
    # context = {
    #     "user": user,
    #     "countries": countries,
    #     "current_country": user.id_country
    # }
    # return  render(request, 'user/account.html', context)
    if request.method == "POST":
        form = UpdateUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password")
            if password:
                user.set_password(password)
            user.save()
            return redirect("home")
    else:
        form = UpdateUserForm(instance=user)
    return render( request,"user/account.html",{'form': form})
# def is_admin(user):
#     return user.is_authenticated and user.is_staff
# @user_passes_test(is_admin)
# def list_user(request):
#     users = CustomUser.objects.all().order_by("-id")
#     return render(request, "user/list_user.html",{"users":users})
# @user_passes_test(is_admin)
# def edit_user(request,id):
#     user_edit = get_object_or_404(CustomUser,id=id, is_staff=False)
#     if request.method == "POST":
#         form = AdminUpdateUserForm(request.POST, request.FILES, instance=user_edit)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Cập nhật thông tin thành công!")
#             return redirect("list_user")
#     else:
#         form = AdminUpdateUserForm(instance=user_edit)
#     context = {
#         "form": form,
#          "user_edit": user_edit
#     }
#     return render(request, "user/edit_user.html", context)
