from django.contrib import admin
from .models import Producer, Category, Article, Comment


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    """docstring for ."""
    list_display = ('category', 'producer', 'model', 'image', 'price',
                    'available')
    list_filter = ('category', 'producer', 'price', 'available')
    prepopulated_fields = {'slug': ('model',)}

admin.site.register(Article, ArticleAdmin)


class ProducerAdmin(admin.ModelAdmin):
    """docstring for ."""
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Producer, ProducerAdmin)


class CategoryAdmin(admin.ModelAdmin):
    """docstring for ."""
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'article', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')

admin.site.register(Comment, CommentAdmin)
