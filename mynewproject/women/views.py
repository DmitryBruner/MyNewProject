from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import *
from .models import *

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'add_page'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Войти', 'url_name': 'login'},


]

class WomenHome(ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Главная страница'} #формирует статический контент
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  #получаем контекст из WomenHome иначе мы потеряем эти данные
        context['menu'] = menu
        context['cat_selected'] = 0
        #context['title'] = 'Главная страница'
        return context
    def get_queryset(self):
        return Women.objects.filter(is_published=True)
# def index(request):
#     posts = Women.objects.all()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#
#     return render(request, 'women/index.html', context=context)


class ShowPost(DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  #получаем контекст из WomenHome иначе мы потеряем эти данные
        context['menu'] = menu
        context['title'] = context['post']
        return context


# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat, #не работает. почему не могу понять
#     }
#     return render(request, 'women/post.html', context=context)



class WomenCategory(ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False #работает когда у нас нет записей в коллекции
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  #получаем контекст из WomenHome иначе мы потеряем эти данные
        context['menu'] = menu
        context['cat_selected'] = context['posts'][0].cat_id #тут ммы получаем все возможные параметры связанные с нашей моделью  context = super().get_context_data(**kwargs) . после обращаемся у первому посту и берем у него номер категории
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        return context
    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)


# def show_category(request, cat_slug):
#     title_cat = Category.objects.get(slug=cat_slug)
#     posts = Women.objects.filter(cat=title_cat.pk)
#
#     if len(posts) == 0:
#         raise Http404()
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': title_cat,
#         'cat_selected': cat_slug,
#     }
#
#     return render(request, 'women/index.html', context=context)


def about(request):
    return render(request, 'women/about.html', {'menu': menu, 'title': 'О сайте'})

class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    #success_url = reverse_lazy('home') если нам нужен редирект не на гет абсолют урл

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  #получаем контекст из WomenHome иначе мы потеряем эти данные
        context['menu'] = menu
        context['title'] = 'Добавление статьи'
        return context


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'women/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})

def login(request):
     return HttpResponse('Обратная связь')

def contact(request):
    return HttpResponse('Авторизация')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')











# пример использования регулярок
# def archive(request, year):
#     if int(year) > 2020:
#         return redirect('home', permanent=False)
#
#     return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")

