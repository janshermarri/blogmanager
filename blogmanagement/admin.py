from django.contrib import admin

# Register your models here.
from . models import *


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['contact', 'date_joined', 'slug']


admin.site.register(Author, AuthorAdmin)

admin.site.register(Post)
admin.site.register(Status)
admin.site.register(Category)
admin.site.register(Comment)

