from django.db import models
from django.urls import reverse

class PublisMeneger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Women(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'
    

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True, db_index=True,)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=Status.choices, default=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT)
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags')
    hasbend = models.OneToOneField('Hasbend', on_delete=models.SET_NULL, null=True,
                                   blank=True, related_name='wumen')


    objects = models.Manager()
    published = PublisMeneger()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        return reverse("post", kwargs={"post_slug": self.slug})
    

class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={"cat_slug": self.slug})
    

class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag
    
    def get_absolute_url(self):
        return reverse('tag', kwargs={"tag_slug": self.slug})
    

class Hasbend(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)

    def __str__(self):
        return self.name