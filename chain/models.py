from django.db import models
from django_countries.fields import CountryField


class Product(models.Model):
    """ Класс для модели Продукт """

    name = models.CharField(
        max_length=150,
        verbose_name="Название продукта",
        help_text="Введите название продукта"
    )
    model = models.CharField(
        unique=True,
        max_length=100,
        verbose_name="Модель продукта",
        help_text="Введите модель продукта"
    )
    product_launch_date = models.DateField(
        verbose_name="Дата выхода продукта на рынок",
        help_text="Введите дату выхода продукта на рынок"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class ElementChain(models.Model):
    """ Класс для модели Звена сети """

    NAME_ELEMENTS = (
        ("завод", "factory"),
        ("розничная сеть", "retail network"),
        ("индивидуальный предприниматель", "individual entrepreneur"),
    )

    name = models.CharField(
        max_length=100,
        verbose_name="Название компании",
        help_text="Введите название компании"
    )
    products = models.ManyToManyField(
        Product,
        related_name="products",
        verbose_name="Продукты",
        help_text="Выберите продукты",
    )
    supplier = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Поставщик",
        help_text="Введите поставщика"
    )
    debt = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Задолженность перед поставщиком",
        help_text="Введите Задолженность перед поставщиком",
        default=0.00
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    name_element_chain = models.CharField(
        max_length=50,
        choices=NAME_ELEMENTS,
        verbose_name="Название элемента сети",
        help_text="Выберите название элемента сети"
    )
    hierarchy_level = models.PositiveSmallIntegerField(
        verbose_name="Уровень иерархии",
        default=0
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"


class Contacts(models.Model):
    """ Класс для модели Контакты """

    element_chain = models.ForeignKey(
        ElementChain,
        on_delete=models.CASCADE,
        verbose_name="Звено сети",
        related_name="contacts",
        blank=True,
        null=True
    )

    email = models.EmailField(verbose_name="Email", help_text="Введите email")
    country = CountryField(blank_label="(select country)", verbose_name="Страна", help_text="Выберите страну")
    city = models.CharField(max_length=40, verbose_name="Город", help_text="Введите город")
    street = models.CharField(max_length=100, verbose_name="Улица", help_text="Введите улицу")
    house_number = models.CharField(max_length=10, verbose_name="Номер дома", help_text="Введите номер дома")

    def __str_(self):
        return f"{self.email} - {self.city}"

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
