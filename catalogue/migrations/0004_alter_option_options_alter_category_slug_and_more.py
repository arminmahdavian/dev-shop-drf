# Generated by Django 5.0.7 on 2024-08-02 08:22

import django.db.models.deletion
import libs.dbs.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0003_remove_productattribute_product_productclass_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='option',
            options={'verbose_name': 'Option', 'verbose_name_plural': 'Option'},
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(allow_unicode=True, unique=True),
        ),
        migrations.AlterField(
            model_name='productattribute',
            name='product_class',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='catalogue.productclass'),
        ),
        migrations.AlterField(
            model_name='productclass',
            name='options',
            field=models.ManyToManyField(blank=True, to='catalogue.option'),
        ),
        migrations.AlterField(
            model_name='productclass',
            name='slug',
            field=models.SlugField(allow_unicode=True, unique=True),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('structure', models.CharField(choices=[('standalone', 'Standalone'), ('parent', 'Parent'), ('child', 'Child')], default='standalone', max_length=16)),
                ('title', models.CharField(blank=True, max_length=128, null=True)),
                ('upc', libs.dbs.fields.UpperCaseCharField(blank=True, max_length=24, null=True, unique=True)),
                ('is_public', models.BooleanField(default=True)),
                ('meta_title', models.CharField(blank=True, max_length=128, null=True)),
                ('meta_description', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(allow_unicode=True, unique=True)),
                ('categories', models.ManyToManyField(related_name='categories', to='catalogue.category')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='catalogue.product')),
                ('product_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='products', to='catalogue.productclass')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='ProductAttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_text', models.TextField(blank=True, null=True)),
                ('value_integer', models.IntegerField(blank=True, null=True)),
                ('value_float', models.FloatField(blank=True, null=True)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.productattribute')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.product')),
                ('value_multi_option', models.ManyToManyField(blank=True, related_name='multi_valued_attribute_value', to='catalogue.optiongroupvalue')),
                ('value_option', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='catalogue.optiongroupvalue')),
            ],
            options={
                'verbose_name': 'Attribute Value',
                'verbose_name_plural': 'Attribute Values',
                'unique_together': {('product', 'attribute')},
            },
        ),
        migrations.AddField(
            model_name='product',
            name='attributes',
            field=models.ManyToManyField(through='catalogue.ProductAttributeValue', to='catalogue.productattribute'),
        ),
        migrations.CreateModel(
            name='ProductRecommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.PositiveSmallIntegerField(default=0)),
                ('primary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='primary_recommendation', to='catalogue.product')),
                ('recommendation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.product')),
            ],
            options={
                'ordering': ('primary', '-rank'),
                'unique_together': {('primary', 'recommendation')},
            },
        ),
        migrations.AddField(
            model_name='product',
            name='recommended_products',
            field=models.ManyToManyField(blank=True, through='catalogue.ProductRecommendation', to='catalogue.product'),
        ),
    ]
