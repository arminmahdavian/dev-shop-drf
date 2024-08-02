from django.db import models


# Create your models here.


class StockRecord(models.Model):
    product = models.ForeignKey('catalogue.Product', on_delete=models.CASCADE, related_name='stockrecords')
    sku = models.CharField(max_length=64, blank=True, null=True, unique=True)
    buy_price = models.PositiveIntegerField(null=True, blank=True)
    sale_price = models.PositiveIntegerField(null=True, blank=True)
    num_stock = models.PositiveIntegerField(default=0)
    threshold_low_stack = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        pass








