# Generated by Django 5.0.1 on 2024-05-14 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EM_app', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addresses',
            name='phone',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='addresses',
            name='pincode',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_dim',
            field=models.CharField(choices=[('12x15', '12X15'), ('12x18', '12X18'), ('16x24', '16X24'), ('20x30', '20X30'), ('12x8', '12X8')], max_length=20),
        ),
    ]