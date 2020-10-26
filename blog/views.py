from django.views.generic import CreateView, UpdateView, ListView, DetailView, TemplateView
from django.views.generic.edit import FormMixin
from django.http import Http404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.urls import reverse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.signals import post_save
from django.utils.text import slugify
from taggit.views import TagListMixin
from .models import (
    Post,
    Dungeon,
)
from .forms import CreatePostForm, CreateCommentForm

class IndexView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = Post
    template_name = 'blog/index.html'
    paginate_by = 10 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Post_list'] = Post.objects.all()
        context['Dungeon_list'] = Dungeon.objects.all()
        return context


class PostDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    form_class = CreateCommentForm

    def get_success_url(self):
        return reverse('blog:postdetail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['form'] = CreateCommentForm(initial={'post': self.object})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = self.object
            comment.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(PostDetailView, self).form_valid(form)


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = CreatePostForm
    model = Post
    template_name = "blog/post_create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.dungeon = Dungeon.objects.get(id = int(self.request.POST['dungeon']))
        print(self.request.POST['tags'])
        print(self.request.POST['tags'].split(","))
        self.object.save()
        for i in self.request.POST['tags'].split(","):
            self.object.tags.add(i)
        self.object.save()
        return redirect('blog:postdetail', pk=self.object.pk);

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Dungeon_list'] = Dungeon.objects.all()
        return context


class SearchPostView(ListView):
    model = Post
    template_name = 'blog/search_post.html'

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        lookups = (
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query) |
                Q(dungeon__name__icontains=query)
        )
        if query is not None:
            qs = super().get_queryset().filter(lookups).distinct()
            return qs
        qs = super().get_queryset()
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context