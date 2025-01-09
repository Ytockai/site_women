from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from .forms import AddPostForm, UpLoadsFileForm
from .models import Women, Category, TagPost

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]


class WomenHome(ListView):
	template_name = 'women/index.html'
	context_object_name = "posts"
	extra_context = {
		'title':'Главная страница',
		'menu': menu,
		'cat_selected': 0,
	}

	def get_queryset(self):
		return Women.published.all().select_related("cat")

def handle_uploaded_file(f):
    with open(f"uploads/{f.name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def about(request):
    if request.method == "POST":
        form = UpLoadsFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(form.cleaned_data['file'])
    else:
        form = UpLoadsFileForm()
    return render(request, 'women/about.html', {'title': 'О сайте', 'form': form})


class ShowPost(DetailView):
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        context['menu'] = menu
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(View):
    def get(self, request):
        form = AddPostForm()
        data = {
        "menu":menu,
        "title": "Добавление статьи",
        "form": form,
        }
        return render(request, 'women/addpage.html', data)
    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        data = {
        "menu":menu,
        "title": "Добавление статьи",
        "form": form,
        }
        return render(request, 'women/addpage.html', data)


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


class WomenCategory(ListView):
	template_name = 'women/index.html'
	context_object_name = "posts"
	allow_empty = False #если нет нужного слага, то выведет ошибку 404

	def get_queryset(self):
		return Women.published.filter(cat__slug=self.kwargs["cat_slug"]).select_related("cat")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		cat = context['posts'][0].cat
		context['title'] = 'Категория - ' + cat.name
		context['menu'] = menu
		context['cat_selected'] = cat.pk
		return context

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class TagPostList(ListView):
    template_name = 'women/index.html'
    context_object_name = "posts"
    allow_empty = False 

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        context['title'] = 'Тег:' + tag.tag
        context['menu'] = menu
        context['cat_selected'] = None
        return context

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs["tag_slug"]).select_related("cat")
