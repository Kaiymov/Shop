from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Comment, Product, CategoryBrand, CustomUser


@admin.register(CustomUser)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'username', 'email')
    list_display_links = ('first_name', 'username')
    search_fields = ('phone',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('category', 'category_brand', 'title', 'status', 'time_create', 'image_show')
    list_display_links = ('category', 'category_brand', 'title')
    search_fields = ('title', 'price')
    list_editable = ('status',)
    list_filter = ('title', 'status', 'time_create',)

    def image_show(self, obj):
        if obj.image:
            return mark_safe("<img src='{}'  height='60' width='60'/>".format(obj.image.url))
        return 'Добавьте картину'
    
    image_show.__name__ = 'Картина'

    
@admin.register(Category)   
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Comment)

@admin.register(CategoryBrand)
class CategoryBrendAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
