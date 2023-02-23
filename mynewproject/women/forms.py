from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *

#Форма с привязкой к моделе
class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Категория не выбрана'
    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 40, 'rows': 10}),
        }
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина строки превышает 200 символов')
        else:
            return title

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

#добавляем форму без привязки к модели
# class AddPostForm(forms.Form):
#     title = forms.CharField(max_length=255, label='Заголовок', widget=forms.TextInput(attrs={'class': 'form-input'}))
#     slug = forms.SlugField(max_length=255, label='URL')
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label='Контент')
#     is_published = forms.BooleanField(label='Публикация', required=False, initial=True)
#     cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категории', empty_label='Категория не выбрана')