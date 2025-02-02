from django.contrib import admin

from .models import Cat, CatColor

# Register your models here.
admin.site.register(Cat)
admin.site.register(CatColor)