from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
import json
import os
from django.conf import settings
from .models import Product
from django.contrib import messages


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
@login_required
def update_product(request,id):
    product = get_object_or_404(Product, id=id, user = request.user)
    if product.images:
        try:
            old_images = json.loads(product.images)
        except:
            old_images = []
    else:
        old_images = []
    if request.method == "GET":
        form = ProductForm(instance=product)
        context = {
            "form": form,
            "product": product,
            "old_images": old_images
        }
        return render(request, "product/update_product.html",context)
    form = ProductForm(request.POST, request.FILES, instance=product)
    if form.is_valid():
        # Nhận ảnh muốn xóa
        delete_images = request.POST.getlist("delete_images")
        # Xóa ảnh khỏi danh sách cũ
        new_old_images = []
        for image in old_images:
            if image not in delete_images:
                new_old_images.append(image)
        old_images = new_old_images
        # Lấy ảnh mới 
        new_images = request.FILES.getlist("images")
        total_images = len(old_images)+len(new_images)
        if total_images > 3:
            form.add_error("images","Tổng số hình ảnh sau khi cập nhật không được vượt quá 3 ảnh!")
            context = {
                "form": form,
                "product": product,
                "old_images": old_images
            }
            return render(request, "product/update_product.html", context)
        for image in delete_images:
            image_path = os.path.join(settings.MEDIA_ROOT, image)
            if os.path.exists(image_path):
                os.remove(image_path)
        for image in new_images:
            image_path = os.path.join(settings.MEDIA_ROOT,"product", image.name)
            os.makedirs(
                os.path.dirname(image_path),
                exist_ok=True
            )
            with open(image_path,"wb+") as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            old_images.append("product/"+image.name)
        # reset trước khi lưu
        old_images = list(old_images)
        # lưu product
        product = form.save(commit=False)
        product.images = json.dumps(old_images)
        product.save()
        messages.success(request,"Cập nhật sản phẩm thành công")
        return redirect("my_product")
    context ={
        "form": form,
        "product": product,
        "old_images": old_images
    }
    return render(request,"product/update_product.html", context)
@login_required
def delete_product(request, id):
    product = get_object_or_404(Product, id=id, user = request.user)
    # Chỉ cho phép post
    if request.method == "POST":
        product.delete()
        messages.success(request, "Delete product successfully!")
    return redirect("my_product")


    

# Create your views here.
