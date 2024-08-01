from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from .models import Category, Product, Option, ProductAttribute


# Register your models here.


class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(Category)
    # list_display = ('title', 'id', 'description', 'slug', 'is_public')
    prepopulated_fields = {"slug": ("title",)}
    # order_by = ('id',)


admin.site.register(Option)


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 2

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'require_shipping', 'track_stock', 'attribute_count')
    list_filter = ('require_shipping', 'track_stock')
    inlines =[ProductAttributeInline]

    def attribute_count(self, obj):
        return obj.attributes.count()



admin.site.register(Category, CategoryAdmin)



