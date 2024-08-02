import hashlib

from django.db import models
from django.utils.text import slugify
from treebeard.mp_tree import MP_Node
from libs.dbs.fields import UpperCaseCharField

from catalogue.managers import CategoryQuerySet


# Create your models here.


class Category(MP_Node):
    title = models.CharField(max_length=255, db_index=True)
    description = models.CharField(max_length=2048, null=True, blank=True)
    is_public = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, allow_unicode=True)

    objects = CategoryQuerySet.as_manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class OptionGroup(models.Model):
    title = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Option Group"
        verbose_name_plural = "Option Groups"


class OptionGroupValue(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    group = models.ForeignKey(OptionGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Option Group Value"
        verbose_name_plural = "Option Group Values"


class ProductClass(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    description = models.CharField(max_length=2048, null=True, blank=True)
    slug = models.SlugField(unique=True, allow_unicode=True)

    track_stock = models.BooleanField(default=True)
    require_shipping = models.BooleanField(default=True)

    options = models.ManyToManyField('Option', blank=True)

    @property
    def has_attribute(self):
        return self.attributes.exists()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Product Class"
        verbose_name_plural = "Product Classes"


class ProductAttribute(models.Model):
    class AttributeTypeChoice(models.TextChoices):
        text = 'text'
        integer = 'integer'
        float = 'float'
        option = 'option'
        multi_option = 'multi_option'

    product_class = models.ForeignKey(ProductClass, on_delete=models.CASCADE, null=True, related_name='attributes')
    title = models.CharField(max_length=64)
    type = models.CharField(max_length=16, choices=AttributeTypeChoice.choices, default=AttributeTypeChoice.text)
    option_group = models.ForeignKey(OptionGroup, on_delete=models.PROTECT, null=True, blank=True)
    required = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Product Attribute"
        verbose_name_plural = "Product Attributes"


class Option(models.Model):
    class OptionTypeChoice(models.TextChoices):
        text = 'text'
        integer = 'integer'
        float = 'float'
        option = 'option'
        multi_option = 'multi_option'

    title = models.CharField(max_length=64)
    type = models.CharField(max_length=16, choices=OptionTypeChoice.choices, default=OptionTypeChoice.text)
    option_group = models.ForeignKey(OptionGroup, on_delete=models.PROTECT, null=True, blank=True)
    required = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Option"
        verbose_name_plural = "Option"


class Product(models.Model):

    class ProductTypeChoice(models.TextChoices):
        standalone = 'standalone'
        parent = 'parent'
        child = 'child'

    structure = models.CharField(max_length=16, choices=ProductTypeChoice.choices, default=ProductTypeChoice.standalone)
    parent = models.ForeignKey("self", related_name="children", on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=128, null=True, blank=True)
    upc = UpperCaseCharField(max_length=24, unique=True, null=True, blank=True)
    is_public = models.BooleanField(default=True)
    meta_title = models.CharField(max_length=128, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)

    slug = models.SlugField(unique=True, allow_unicode=True)

    product_class = models.ForeignKey(ProductClass, on_delete=models.PROTECT, null=True, blank=True,
                                      related_name='products')
    attributes = models.ManyToManyField(ProductAttribute, through='ProductAttributeValue')
    recommended_products = models.ManyToManyField('catalogue.Product', through='ProductRecommendation', blank=True)
    categories = models.ManyToManyField(Category, related_name='categories')


    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)

    value_text = models.TextField(null=True, blank=True)
    value_integer = models.IntegerField(null=True, blank=True)
    value_float = models.FloatField(null=True, blank=True)
    value_option = models.ForeignKey(OptionGroupValue, on_delete=models.PROTECT, null=True, blank=True)
    value_multi_option = models.ManyToManyField(OptionGroupValue, blank=True,
                                                related_name='multi_valued_attribute_value')

    class Meta:
        verbose_name = "Attribute Value"
        verbose_name_plural = "Attribute Values"
        unique_together = ('product', 'attribute')


class ProductRecommendation(models.Model):
    primary = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='primary_recommendation')
    recommendation = models.ForeignKey(Product, on_delete=models.CASCADE)
    rank = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ('primary', 'recommendation')
        ordering = ('primary', '-rank')


class Image(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True)
    image = models.ImageField(width_field='width', height_field='height', upload_to='images/')

    width = models.IntegerField(editable=False)
    height = models.IntegerField(editable=False)

    file_hash = models.CharField(max_length=40, db_index=True)
    file_size = models.PositiveIntegerField(null=True)

    focal_point_x = models.PositiveIntegerField(null=True, blank=True)
    focal_point_y = models.PositiveIntegerField(null=True, blank=True)
    focal_point_width = models.PositiveIntegerField(null=True, blank=True)
    focal_point_height = models.PositiveIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):

        self.file_size = self.image.size

        hasher = hashlib.sha1()
        for chunk in self.image.file.chunks():
            hasher.update(chunk)
        self.file_hash = hasher.digest()

        super().save(*args, **kwargs)


