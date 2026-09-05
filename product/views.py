from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
import json
import os
from django.conf import settings
from .models import Product, History, Category, Brand
from django.contrib import messages
from django.http import JsonResponse
from user.form import RegisterUser
from django.contrib.auth import login
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db import connection
from django.core.paginator import Paginator


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
@login_required
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    if product.images:
        product.image_filenames = json.loads(product.images)
    else:
        product.image_filenames = []
    return render(request, "product/product_detail.html", {"product":product})

def add_to_cart(request):
    product_id = request.POST.get("product_id")
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get("cart",{})
    product_id = str(product_id)
    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] =1
    request.session["cart"] = cart
    request.session.modified = True
    cart_count = sum(cart.values())
    return JsonResponse({
        "success":True,
        "cart_count": cart_count
    })
def cart(request):
    # return render(request, "product/cart.html")
    cart = request.session.get("cart", {})
    cart_items = []
    cart_total = 0
    for product_id, quantity in cart.items():
        product = Product.objects.filter(id=product_id).first()
        if product:
            if product.images:
                image_filenames = json.loads(product.images)
            else:
                image_filenames = []
            item_total = product.price * quantity
            cart_total += item_total
            cart_items.append({
                "product": product,
                "quantity": quantity,
                "images": image_filenames,
                "item_total": item_total
            })
    return render(request, "product/cart.html", {"cart_items": cart_items, "cart_total":cart_total})
def update_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        action = request.POST.get("action")
        cart = request.session.get('cart',{})
        product_id = str(product_id)
        if product_id in cart:
            if action == "increase":
                cart[product_id] += 1
            elif action == "decrease":
                if cart[product_id] > 1:
                    cart[product_id] -= 1
                else:
                    return JsonResponse({
                        "success": False,
                        "message": "Số lượng sản phẩm tối thiểu là 1!"
                    })
            elif action == "delete":
                del cart[product_id]
                # request.session['cart'] = cart
                # request.session.modified = True
                # return JsonResponse({
                #     "success":True,
                #     "product_id": product_id,
                #     "action": "delete",
                # })
            request.session['cart'] = cart
            request.session.modified = True
            # Tính tổng toàn bộ để gửi ajax
            cart_total = 0
            for id, quantity in cart.items():
                product = Product.objects.filter(id=id).first()
                if product:
                    cart_total += product.price * quantity
            if action == "delete":
                return JsonResponse({
                    "success": True,
                    "action": action,
                    "product_id": product_id,
                    "cart_total": cart_total
                })
            product = get_object_or_404(Product, id=product_id)
            quantity = cart[product_id]
            item_total = product.price * quantity
            return JsonResponse({
                "success": True,
                "quantity": quantity,
                "item_total": item_total,
                "cart_total": cart_total
            })
    return JsonResponse({
        "success": False
    })
def checkout(request):
    cart = request.session.get("cart",{})
    cart_items = []
    cart_subtotal = 0 
    for product_id, quantity in cart.items():
        product = Product.objects.filter(id=product_id).first()
        if product:
            images = json.loads(product.images) if product.images else []
            item_total = product.price * quantity
            cart_subtotal += item_total
            cart_items.append({
                "product": product,
                "quantity": quantity,
                "images": images,
                "item_total": item_total
            })
    tax = 2
    cart_total = cart_subtotal + tax
    register_form = RegisterUser()
    if request.method == "POST":
        # if not request.user.is_authenticated:
        #     messages.warning(request, "VUi lòng đăng nhập trước khi đặt hàng!")
        #     return redirect("checkout")
        if not cart_items:
            messages.warning(request, "Giỏ hàng của bạn đang rỗng!")
            return redirect("checkout")
        if request.user.is_authenticated:
            name = request.POST.get("name", "").strip()
            phone = request.POST.get("phone", "").strip()
            email = request.user.email
            if not name or not phone:
                messages.error(request, "Vui lòng nhập số điện thoại hoặc tên trước khi đặt hàng!")
            elif not email:
                messages.error(request, "Tài khoản của bạn chưa có email!")
            else:
                History.objects.create(
                    user = request.user,
                    name = name,
                    email = email, 
                    phone = phone,
                    price = cart_total
                )
                send_order_email(
                    email=email,
                    name=name,
                    phone=phone,
                    cart_items=cart_items,
                    cart_subtotal=cart_subtotal,
                    tax=tax,
                    cart_total=cart_total
                )
                request.session["cart"] = {}
                request.session.modified = True
                messages.success(request, "Đặt hàng thành công, Vui lòng kiểm tra email!")
                return redirect("checkout")
        else:
            register_form = RegisterUser(request.POST)
            # Do ban đầu form đăng ký kh có số điện thoại nên lấy riêng 
            phone = request.POST.get("phone","")
            if not phone:
                messages.error(request, "Vui lòng nhập số điện thoại!")
            elif register_form.is_valid():
                user = register_form.save(commit=False)
                user.is_superuser = False
                user.is_staff = False
                user.set_password(register_form.cleaned_data["password"])
                user.save()
                login(request, user)
                fullname = (f"{user.first_name}"f"{user.last_name}").strip()
                if not fullname:
                    fullname = user.username
                History.objects.create(
                    user = user,
                    email = user.email,
                    phone = phone, 
                    name = fullname,
                    price = cart_total
                )
                send_order_email(
                    email=email,
                    name=name,
                    phone=phone,
                    cart_items=cart_items,
                    cart_subtotal=cart_subtotal,
                    tax=tax,
                    cart_total=cart_total
                )
                request.session["cart"]={}
                request.session.modified = True
                messages.success(request, "Đặt hàng thành công, Vui lòng kiểm tra email!")
                return redirect("checkout")
    context = {
        "cart_items": cart_items,
        "cart_subtotal": cart_subtotal,
        "tax": tax,
        "cart_total": cart_total,
        "register_form": register_form
    }

    return render(request, "product/checkout.html", context)
def send_order_email(email,name,phone,cart_items,cart_subtotal,tax,cart_total):
    subject = "Mail xác nhận đặt hàng!"
    context = {
        "name": name,
        "phone": phone,
        "cart_items": cart_items,
        "cart_subtotal": cart_subtotal,
        "tax": tax,
        "cart_total": cart_total
    }
    html_content = render_to_string("product/order_email.html", context)
    text_content = f"""
        Xin chào {name}
        Cảm ơn vì đã đặt hàng!
        Phone: {phone}
        Total:  ${cart_total}"""
    email_message = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=None,
        to=[email]
    )
    email_message.attach_alternative(
        html_content,
        "text/html"
    )
    email_message.send()
def search_product(request):
    keyword = request.GET.get("q","").strip()
    products = []
    if keyword:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id,name,price,images FROM product_product
                WHERE name LIKE %s""",
                [f"%{keyword}%"]
            )
            rows = cursor.fetchall()
        for row in rows:
            images = []
            if row[3]:
                images = json.loads(row[3])
            products.append({
                "id": row[0],
                "name": row[1],
                "price": row[2],
                "images": images
            })
    context = {
        "products": products,
        "keyword": keyword
    }
    return render(request, "product/search.html", context)
def search_advanced(request):
    name = request.GET.get("name", "").strip()
    price = request.GET.get("price", "")
    category_id = request.GET.get("category", "")
    brand_id = request.GET.get("brand", "")
    status = request.GET.get("status", "")
    categories = Category.objects.all()
    brands = Brand.objects.all()

    sql = """ SELECT id, name, price, images, category_id, brand_id, status FROM product_product 
    WHERE 1 = 1"""
    p = []
    if name: 
        sql += """ AND LOWER(name) LIKE LOWER(%s)"""
        p.append(f"%{name}%")
    if price:
        if price == "0-100":
            sql += """ AND price BETWEEN %s AND %s"""
            p.extend([0,100])
        elif price == "100-500":
            sql += """ AND price BETWEEN %s AND %s"""
            p.extend([100,500])
        elif price == "500-1000":
            sql += """ AND price BETWEEN %s AND %s"""
            p.extend([500,1000])
        elif price =="1000-2000":
            sql += """ AND price BETWEEN %s AND %s"""
            p.extend([1000,2000])
        elif price == "2000+":
            sql += """ AND price >= %s"""
            p.append(2000)
    if category_id:
        sql += """ AND category_id = %s"""
        p.append(category_id)
    if brand_id:
        sql += """ AND brand_id = %s"""
        p.append(brand_id)
    if status:
        sql += """ AND status = %s"""
        p.append(status)
    sql += """ ORDER BY id DESC"""
    with connection.cursor() as cursor:
        cursor.execute(sql, p)
        rows = cursor.fetchall()
    products = []
    for row in rows: 
        images = []
        if row[3]:
            images = json.loads(row[3])
        products.append({
            "id": row[0],
            "name": row[1],
            "price": row[2],
            "images": images,
            "category_id": row[4],
            "brand_id": row[5],
            "status": row[6]
        })
    paginator = Paginator(products,2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number) 
    # print("SQL:", sql)
    # print("PARAMS:", p)
    # print("ROWS:", rows)
    context = {
        # "products": products,
        "page_obj": page_obj,
        "categories": categories,
        "brands": brands
    }
    return render(request, "product/search_advanced.html", context)
def filter_price(request):
    min_price = request.GET.get("min_price",0)
    max_price = request.GET.get("max_price",200000)
    sql = """ SELECT id,name,price,images,status FROM product_product WHERE price BETWEEN %s AND %s 
    ORDER BY id DESC """
    with connection.cursor() as cursor:
        cursor.execute(sql, [min_price,max_price])
        rows = cursor.fetchall() 
    products = []
    for row in rows:
        images = []
        if row[3]:
           images = json.loads(row[3])
        products.append({
            "id": row[0],
            "name": row[1],
            "price": row[2],
            "images": images,
            "status": row[4]
        })
    print("MIN_PRICE:", min_price)
    print("MAX_PRICE:", max_price)
    print("PRODUCTS:", rows)
    return JsonResponse({
        "products": products 
    })



# Create your views here.
