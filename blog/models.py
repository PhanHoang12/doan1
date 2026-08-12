from django.db import models
from django.conf import settings

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
# Create your models here.
