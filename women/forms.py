from django import forms
from .models import Category, Hasbend


class AddPostFroms(forms.Form):
    title = forms.CharField(max_length=255, label="Заголовок")
    slug = forms.SlugField(max_length=255, label="SLUG")
    content = forms.CharField(widget=forms.Textarea(), required=False, label="Текст")
    is_published = forms.BooleanField(label="Опубликовать")
    cat = forms.ModelChoiceField(queryset=Category.objects.all(),empty_label="Категория не выбрана", label="Категория")
    hasbend = forms.ModelChoiceField(queryset=Hasbend.objects.all(), required=False, empty_label="Не замужем", label="Муж")