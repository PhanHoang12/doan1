from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
import json
import os
from django.conf import settings
from .models import Product

@login_required
def created_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            images = form.cleaned_data.get("images")
            image_filenames = []
            if images:
                product_folder = os.path.join(settings.MEDIA_ROOT,"product")
                os.makedirs(product_folder, exist_ok=True)
                for image in images:
                    image_path = os.path.join(product_folder,image.name)
                    with open(image_path, "wb+") as destination:
                        for chunk in image.chunks():
                            destination.write(chunk)
                    image_filenames.append("product/"+ image.name)
            product.images = json.dumps(image_filenames)
            product.save()
            return redirect("my_product")
    else:
        form = ProductForm()
    return render(request, "product/create_product.html", {"form":form})
@login_required
def my_product(request):
    products = Product.objects.filter(user=request.user).order_by('-created_at')
    for product in products:
        if product.images:
            product.image_filenames = json.loads(product.images)
        else:
            product.image_filenames = []
    return render(request,'product/my_product.html',{'products': products})

# Create your views here.
