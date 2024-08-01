from django.contrib import admin
from django.db.models import Count
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


class AttributeCountFilter(admin.SimpleListFilter):
    title = "Attribute Count"
    parameter_name = "attr_count"

    def lookups(self, request, model_admin):
        return [
            ('more_5', 'More than 5'),
            ('lower_5', 'Lower than 5'),
        ]

    def queryset(self, request, queryset):
        if self.value() == "more_5":
            return queryset.annotate(attr_count=Count('attributes')).filter(attr_count__gt=1)
        if self.value() == "lower_5":
            return queryset.annotate(attr_count=Count('attributes')).filter(attr_count__lt=1)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'require_shipping', 'track_stock', 'attribute_count')
    list_filter = ('require_shipping', 'track_stock', AttributeCountFilter)
    inlines =[ProductAttributeInline]
    actions = ['enable_track_stock', 'disable_track_stock']
    prepopulated_fields = {"slug": ("title",)}


    def attribute_count(self, obj):
        return obj.attributes.count()

    def enable_track_stock(self, request, queryset):
        queryset.update(track_stock=True)

    def disable_track_stock(self, request, queryset):
        queryset.update(track_stock=False)



admin.site.register(Category, CategoryAdmin)



