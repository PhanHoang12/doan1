from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Blog
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
    context = {
        "blog": blog
    }
    return render(request, "blog/blog_detail.html", context)
