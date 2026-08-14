from django.db import models
from django.conf import settings
from django.utils import timezone

class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()
    image = models.ImageField(upload_to="blog/anh_upload", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
class Rate(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="rates")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        # dùng để chặn user đánh giá nhiều dòng trong 1 blog 
        unique_together = ("blog", "user") 
    def __str__(self):
        return f'{self.user}, {self.blog}, {self.score}'    
class Comments(models.Model):
    comment = models.TextField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    # author_name = models.TextField()
    # author_image = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    level = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.author} - {self.blog}"
    # Tại sao cần parent : ví dụ dữ liệu cmt 1 là cmt cha thì : id = 1; parent_id = null, level = 0 sau khi reply thì id = 2; parent_id=1, level =1, tiếp tục thì id = 3; parent_id = 1; level vẫn bằng 1



# Create your models here.
