# Generated by Django 4.2 on 2023-06-14 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TiendaApp', '0004_subcategoriaproducto_producto_subcategoria'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subcategoriaproducto',
            options={'verbose_name': 'subcategoriaProd', 'verbose_name_plural': 'subcategoriasProd'},
        ),
    ]