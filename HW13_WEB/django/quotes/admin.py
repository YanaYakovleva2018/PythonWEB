from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Tag, Author, Quote

admin.site.register(Tag)
admin.site.register(Author)
admin.site.register(Quote)
