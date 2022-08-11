from django.db import models

class Post(models.Model):
    title=models.CharField(max_length=30)
    content=models.TextField()
    head_image=models.ImageField(upload_to='blog/images/%Y/%m/%d/',blank=True) #blank는 null값을 안올려도 괜찮냐 라고 물어보는 것
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    #author: 추후 작성 예정

    def __str__(self):
        return f'[{self.pk}]{self.title}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}'

