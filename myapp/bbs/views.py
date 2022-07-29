from django.shortcuts import render
from django.http import HttpResponse
from .models import Article
from django.views import generic

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from django.db.models import Q # 追加

def index(request):
    return HttpResponse('Hello Django')
 
def detail(request, id):
    return HttpResponse('detail ' + str(id))
 
def create(request):
    return HttpResponse('create')

class UpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Article
    fields = ['content', 'title', ]
 
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
 
        if obj.author != self.request.user:
            raise PermissionDenied('You do not have permission to edit.')
 
        return super(UpdateView, self).dispatch(request, *args, **kwargs)

class DeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Article
    success_url = reverse_lazy('bbs:index')

class IndexView(generic.ListView):
    def get_queryset(self):
        q_word = self.request.GET.get('query')
 
        # チェックボックスにチェックが入っている項目だけを検索対象とする
        selected_title = self.request.GET.get('title')
        selected_article = self.request.GET.get('article')
 
        if q_word:
            if selected_title and selected_article:
                object_list = Article.objects.filter(
                    Q(title__icontains=q_word) | Q(content__icontains=q_word))
            elif selected_title:
                object_list = Article.objects.filter(Q(title__icontains=q_word))
            else: # 投稿内容のみ、または両方ともチェックされていない場合は投稿内容のみを検索する
                object_list = Article.objects.filter(Q(content__icontains=q_word))
        else:
            object_list = Article.objects.all()
 
        return object_list
 
class DetailView(generic.DetailView):
    model = Article

class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Article
    fields = ['content', 'title', ]
 
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateView, self).form_valid(form)