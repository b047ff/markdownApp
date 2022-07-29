from django.db import models
from django.urls import reverse
from mdeditor.fields import MDTextField # 追加
 
class Article(models.Model):
    title = models.CharField(max_length = 200)
    content = MDTextField(max_length=1000) # 変更
 
    author = models.ForeignKey(
        'auth.User',
        on_delete = models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return self.content
 
    def get_absolute_url(self):
        return reverse('bbs:detail', kwargs={'pk': self.pk})
