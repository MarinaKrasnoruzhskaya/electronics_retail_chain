# Generated by Django 5.1.3 on 2024-12-02 20:45

import django.db.models.deletion
import django_countries.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Введите название продукта",
                        max_length=150,
                        verbose_name="Название продукта",
                    ),
                ),
                (
                    "model",
                    models.CharField(
                        help_text="Введите модель продукта",
                        max_length=100,
                        unique=True,
                        verbose_name="Модель продукта",
                    ),
                ),
                (
                    "product_launch_date",
                    models.DateField(
                        help_text="Введите дату выхода продукта на рынок",
                        verbose_name="Дата выхода продукта на рынок",
                    ),
                ),
            ],
            options={
                "verbose_name": "Продукт",
                "verbose_name_plural": "Продукты",
            },
        ),
        migrations.CreateModel(
            name="ElementChain",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Введите название компании",
                        max_length=100,
                        verbose_name="Название компании",
                    ),
                ),
                (
                    "debt",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        help_text="Введите Задолженность перед поставщиком",
                        max_digits=10,
                        verbose_name="Задолженность перед поставщиком",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Время создания"
                    ),
                ),
                (
                    "name_element_chain",
                    models.CharField(
                        choices=[
                            ("завод", "factory"),
                            ("розничная сеть", "retail network"),
                            (
                                "индивидуальный предприниматель",
                                "individual entrepreneur",
                            ),
                        ],
                        help_text="Выберите название элемента сети",
                        max_length=50,
                        verbose_name="Название элемента сети",
                    ),
                ),
                (
                    "hierarchy_level",
                    models.PositiveSmallIntegerField(
                        default=0, verbose_name="Уровень иерархии"
                    ),
                ),
                (
                    "supplier",
                    models.ForeignKey(
                        blank=True,
                        help_text="Введите поставщика",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="chain.elementchain",
                        verbose_name="Поставщик",
                    ),
                ),
                (
                    "products",
                    models.ManyToManyField(
                        help_text="Выберите продукты",
                        related_name="products",
                        to="chain.product",
                        verbose_name="Продукты",
                    ),
                ),
            ],
            options={
                "verbose_name": "Поставщик",
                "verbose_name_plural": "Поставщики",
            },
        ),
        migrations.CreateModel(
            name="Contacts",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        help_text="Введите email", max_length=254, verbose_name="Email"
                    ),
                ),
                (
                    "country",
                    django_countries.fields.CountryField(
                        help_text="Выберите страну", max_length=2, verbose_name="Страна"
                    ),
                ),
                (
                    "city",
                    models.CharField(
                        help_text="Введите город", max_length=40, verbose_name="Город"
                    ),
                ),
                (
                    "street",
                    models.CharField(
                        help_text="Введите улицу", max_length=100, verbose_name="Улица"
                    ),
                ),
                (
                    "house_number",
                    models.CharField(
                        help_text="Введите номер дома",
                        max_length=10,
                        verbose_name="Номер дома",
                    ),
                ),
                (
                    "element_chain",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contacts",
                        to="chain.elementchain",
                        verbose_name="Звено сети",
                    ),
                ),
            ],
            options={
                "verbose_name": "Контакт",
                "verbose_name_plural": "Контакты",
            },
        ),
    ]