from django.db import models
from django.urls import reverse

from django_extensions.db.fields import AutoSlugField
from tinymce.models import HTMLField

class Page(models.Model):
    name = models.CharField(max_length=300)

    class Meta:
        abstract = True


class Content(Page):
    content = HTMLField()
    slug = AutoSlugField(populate_from='name')

    def get_absolute_url(self):
        return reverse('page', kwargs={'slug': self.slug})

    def slugify_function(self, content):
        return content.replace(' ', '-').lower()

    def __str__(self):
        return self.name
