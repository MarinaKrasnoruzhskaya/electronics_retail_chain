from django_countries.serializers import CountryFieldMixin
from drf_writable_nested import WritableNestedModelSerializer, UniqueFieldsMixin
from rest_framework import serializers

from chain.models import Contacts, ElementChain, Product


class ContactsSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """ Сериализатор для модели Contacts """

    class Meta:
        model = Contacts
        exclude = ('id', 'element_chain')


class ContactsUpdateSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """ Сериализатор для модели Contacts для изменения """

    id = serializers.IntegerField()

    class Meta:
        model = Contacts
        fields = "__all__"


class ElementChainSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели ElementChain """

    contacts = ContactsSerializer(many=True)
    created_at = serializers.DateTimeField(read_only=True)
    hierarchy_level = serializers.IntegerField(read_only=True)

    class Meta:
        model = ElementChain
        exclude = ('products',)

    def create(self, validated_data):
        """ Создание звена сети и контактов """

        # Задаём значение уровня иерархии
        supplier_data = validated_data.get('supplier')
        if supplier_data:
            validated_data['hierarchy_level'] = supplier_data.hierarchy_level + 1

        # Создаём объект модели Звено сети и объекты модели Контакты
        contacts_data = validated_data.pop('contacts')
        supplier = ElementChain.objects.create(**validated_data)

        for contact_data in contacts_data:
            Contacts.objects.create(element_chain=supplier, **contact_data)

        return supplier


class ElementChainUpdateSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели ElementChain для изменения """

    contacts = ContactsUpdateSerializer(many=True)
    debt = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = ElementChain
        exclude = ('products',)
        read_only_fields = ('debt', 'created_at', 'hierarchy_level')

    def update(self, instance, validated_data):
        """ Метод для изменения звена сети и контактов """

        if validated_data.get('contacts'):
            contacts_data = validated_data.pop('contacts')

            # Обновляем или создаём контакты
            for contact_data in contacts_data:
                # Если задан id контакта, проверяем чтобы это был контакт изменяемого звена цепи и обновляем его
                if contact_data.get('id'):
                    if Contacts.objects.filter(pk=contact_data.get('id'), element_chain=instance).exists():
                        contact = Contacts.objects.get(pk=contact_data.get('id'), element_chain=instance)
                        contact.email = contact_data.get('email', contact.email)
                        contact.country = contact_data.get('country', contact.country)
                        contact.city = contact_data.get('city', contact.city)
                        contact.street = contact_data.get('street', contact.street)
                        contact.house_number = contact_data.get('house_number', contact.house_number)
                        contact.save()
                    else:
                        raise serializers.ValidationError('Попытка изменить чужой контакт')
                # Если не задан id контакта, то создаётся новый контакт для изменяемого звена цепи со всеми полями
                else:
                    if contact_data.get('email') and contact_data.get('country') and contact_data.get('city') and \
                            contact_data.get('street') and contact_data.get('house_number'):
                        Contacts.objects.create(element_chain=instance, **contact_data)
                    else:
                        raise serializers.ValidationError('Необходимо заполнить все поля контакта')

        # Обновляем модель
        instance.name = validated_data.get('name', instance.name)
        instance.supplier = validated_data.get('supplier', instance.supplier)
        instance.name_element_chain = validated_data.get('name_element_chain', instance.name_element_chain)
        instance.save()

        return instance


class ProductSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    """ Сериализатор для модели Product """

    class Meta:
        model = Product
        fields = "__all__"


class ElementChainProductsSerializer(WritableNestedModelSerializer):
    """ Сериализатор для модели ElementChain с продуктами """

    pk = serializers.IntegerField()
    products = ProductSerializer(many=True)

    def create(self, validated_data):
        """ Создание продукта звеном цепи - завод """

        instance = ElementChain.objects.get(pk=validated_data.get('pk'))
        if instance.name_element_chain in ['завод', 'factory']:
            products_data = validated_data.get('products')
            for product_data in products_data:
                product_new = Product.objects.create(**product_data)
                instance.products.add(product_new)
                instance.save()
            return instance
        raise serializers.ValidationError('Продукт может создавать только "завод"')

    def update(self, instance, validated_data):
        """ Добавление продуктов звену цепи с уровнем > 0, если такие продукты есть у supplier"""

        products_data = validated_data.pop('products')

        products_all = Product.objects.all().filter(products__name=instance.name)
        # Звено цепи - завод обновляет свои продукты
        if instance.hierarchy_level == 0:
            for product_data in products_data:
                product_update = Product.objects.get(model=product_data.get('model'))
                product_update.name = product_data.get('name', product_update.name)
                product_update.product_launch_date = product_data.get('product_launch_date',
                                                                      product_update.product_launch_date)
                product_update.save()
        # Звено цепи не завод добавляет себе продукт поставщика уровнем выше
        else:
            for product_data in products_data:
                product_add = Product.objects.get(model=product_data.get('model'))
                if product_add not in products_all:
                    product_all_supplier = Product.objects.all().filter(products__name=instance.supplier.name)
                    if product_add in product_all_supplier:
                        instance.products.add(product_add)
                        instance.save()
                    else:
                        raise serializers.ValidationError('Такого продукта нет у поставщика')

        return instance

    class Meta:
        model = ElementChain
        fields = ('pk', 'products')

