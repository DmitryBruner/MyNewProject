from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from  django.contrib.auth.mixins import LoginRequiredMixin

from .utils import *
from .forms import *
from .models import *


class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Главная страница'} #формирует статический контент
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  #получаем контекст из WomenHome иначе мы потеряем эти данные
        c_def = self.get_user_context(title='Главная страница')
        context = dict(list(context.items())+list(c_def.items()))
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


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  #получаем контекст из WomenHome иначе мы потеряем эти данные
        def_c = self.get_user_context(title=context['post'], cat_selected='pass')
        return dict(list(context.items()) + list(def_c.items()))


# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat, #не работает. почему не могу понять
#     }
#     return render(request, 'women/post.html', context=context)



class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False #работает когда у нас нет записей в коллекции
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  #получаем контекст из WomenHome иначе мы потеряем эти данные
        # context['menu'] = menu
        # context['cat_selected'] = context['posts'][0].cat_id #тут ммы получаем все возможные параметры связанные с нашей моделью  context = super().get_context_data(**kwargs) . после обращаемся у первому посту и берем у него номер категории
        # context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        def_c = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat), cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items()) + list(def_c.items()))
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
    contact_list = Women.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'women/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    login_url = reverse_lazy('home') # перенаправляет наc на выбранную страничку если доступ к этой запрещен
    #raise_exception = True генерит ошибку при попытки доступа к странице
    #success_url = reverse_lazy('home') если нам нужен редирект не на гет абсолют урл

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  #получаем контекст из WomenHome иначе мы потеряем эти данные
        def_c = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items())+list(def_c.items()))


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'women/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})

# def login(request):
#      return HttpResponse('Обратная связь')

class ContactForView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwards):
        context = super().get_context_data(**kwards)
        def_c = self.get_user_context(title='Обратная связь')
        return dict(list(context.items())+list(def_c.items()))

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')



class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        def_c = self.get_user_context(title='Регистрация')
        return dict(list(context.items())+list(def_c.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(title='Авторизация')
        def_c = self.get_user_context(title='Авторизация')
        return dict(list(context.items())+list(def_c.items()))
    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')
# пример использования регулярок
# def archive(request, year):
#     if int(year) > 2020:
#         return redirect('home', permanent=False)
#
#     return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")

