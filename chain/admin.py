from django.contrib import admin
from django.db import transaction
from django.urls import reverse
from django.utils.safestring import mark_safe

from chain.models import Product, Contacts, ElementChain


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Администрирование модели ElementChain """

    list_display = ('name', 'model', 'product_launch_date', )


class ContactInline(admin.TabularInline):
    """ Инлайн для модели Contacts """

    model = Contacts
    extra = 1


class ProductInline(admin.TabularInline):
    """ Инлайн для модели Product"""

    model = Product
    extra = 1


@admin.register(ElementChain)
class ElementChainAdmin(admin.ModelAdmin):
    """ Администрирование модели ElementChain """

    list_display = ('name', 'city', 'supplier_link', 'debt', 'created_at', 'name_element_chain', 'hierarchy_level', )
    readonly_fields = ('created_at', 'hierarchy_level')
    inlines = [ContactInline, ]
    actions = ("clear_debt",)
    list_filter = ('contacts__city',)

    @admin.display(description="Supplier URL")
    def supplier_link(self, obj):
        """ Ссылка на редактирование объекта сети с передачей pk поставщика в URL"""

        if obj.supplier:
            href = reverse("admin:chain_elementchain_change", args=(obj.supplier.pk,))
            return mark_safe('<a href="{}">{}</a>'.format(href, obj.supplier.name))

    @admin.display(description="Город")
    def city(self, obj):
        """ Возвращает город из связанных контактов """

        city = obj.contacts.first().city
        return city

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        """ Метод определяет уровень иерархии звена сети """

        if obj.supplier:
            obj.hierarchy_level = obj.supplier.hierarchy_level + 1
            obj.save()
        super().save_model(request, obj, form, change)

    @admin.action(description="Очистить задолженность перед поставщиком")
    def clear_debt(self, request, queryset):
        """ Для выбранных объектов сети значение задолженность перед поставщиком сделать равной 0.00"""

        queryset.update(debt=0.00)
