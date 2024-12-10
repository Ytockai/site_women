from django import forms
from .models import Category, Hasbend


class AddPostFroms(forms.Form):
    title = forms.CharField(max_length=255)
    slug = forms.SlugField(allow_unicode=True)
    content = forms.CharField(widget=forms.Textarea(), required=False)
    is_published = forms.BooleanField()
    cat = forms.ModelChoiceField(queryset=Category.objects.all())
    hasbend = forms.ModelChoiceField(queryset=Hasbend.objects.all())