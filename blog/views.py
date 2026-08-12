from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Blog, Rate
from django.db.models import Avg
from django.http import JsonResponse
# Create your views here.
def Blog_list(request):
    blog = Blog.objects.all().order_by('-created_at')
    paginator = Paginator(blog,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "blog/blog_list.html", {"page_obj": page_obj})
def blog_detail(request, id):
    blog = get_object_or_404(Blog,id=id)
    #  tạo một dictionary để lưu dữ liệu của biến blog vừa lấy được ở trên gửi sang HTML
    # context = {
    #     "blog": blog
    # }
    # return render(request, "blog/blog_detail.html", context)


    # Update phần sau khi làm blog rate
    result = Rate.objects.filter(blog=blog).aggregate(average = Avg("score"))
    average = result['average'] or 0
    average = round(float(average),1)
    total = Rate.objects.filter(blog=blog).count()
    star = []
    for i in range(1,6):
        if i <= average:
            star.append(True)
        else:
            star.append(False)
    context = {
        "blog": blog,
        "average":average,
        "total": total,
        "star": star
    }
    return render(request, "blog/blog_detail.html", context)
def blog_rate(request):
    # Xử lí chưa đăng nhập
    if not request.user.is_authenticated:
        return JsonResponse({
            "success": False,
            "login_required": True,
            "message": "Vui lòng đăng nhập trước!"
        }, status = 401)
    if request.method == "POST":
        blog_id = request.POST.get("blog_id")
        rate = request.POST.get("rate")
        if not blog_id or not rate:
            return JsonResponse({
                "success": False,
                "message": "Thiếu dữ liệu"
            },status=400)
        try:
            rate = int(rate)
        except ValueError:
            return JsonResponse({
                "success": False,
                "message": "SỐ sao không hợp lệ!"
            }, status = 400)
        if rate < 1 or rate > 5: 
            return JsonResponse({
                "success": False,
                "message": "Số sao phải nằm trong khoảng từ 1 đến 5"
            }, status = 400)
        blog = get_object_or_404(Blog, id = blog_id)
        Rate.objects.update_or_create(
            blog = blog,
            user = request.user,
            defaults={
                "score": rate
            }
        )
        # result = Rate.objects.filter(blog=blog).aggregate(
        #     average = Avg("score")
        # )
        # average = result['average'] or 0
        # average = round(float(average), 1)

        # Tổng lượt đánh giá
        total = Rate.objects.filter(blog=blog).count()
        return JsonResponse({
            "success": True,
            "message": "Đánh giá thành công",
            "rate": rate,
            # "average": round(float(average),1),
            "total": total
        })
        
