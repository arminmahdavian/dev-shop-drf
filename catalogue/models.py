from django.db import models
from django.utils.text import slugify
from treebeard.mp_tree import MP_Node

from catalogue.managers import CategoryQyerySet


# Create your models here.


class Category(MP_Node):
    title = models.CharField(max_length=255, db_index=True)
    description = models.CharField(max_length=2048, null=True, blank=True)
    is_public = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)

    objects = CategoryQyerySet.as_manager()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


    def __str__(self):
        return self.title


