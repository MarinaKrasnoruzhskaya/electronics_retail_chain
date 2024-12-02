from rest_framework.generics import DestroyAPIView, CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from chain.models import ElementChain, Contacts, Product
from chain.permissions import IsActiveUser
from chain.serializers import ElementChainSerializer, ElementChainUpdateSerializer, ContactsSerializer, \
    ElementChainProductsSerializer, ProductSerializer


class ElementChainViewSet(ModelViewSet):
    """ Класс-представление для модели ElementChain """

    queryset = ElementChain.objects.all()
    serializer_class = ElementChainSerializer
    permission_classes = [IsAuthenticated, IsActiveUser, ]

    class Meta:
        model = ElementChain
        fields = "__all__"

    def get_serializer_class(self):
        """ Возвращает сериализатор для получения объекта сети """

        if self.action in ["update", "partial_update"]:
            return ElementChainUpdateSerializer
        return super().get_serializer_class()


class ContactsDestroyAPIView(DestroyAPIView):
    """ Класс-представление для удаления контакта звена сети """

    queryset = Contacts.objects.all()
    lookup_field = "element_chain_id"
    serializer_class = ContactsSerializer
    permission_classes = [IsAuthenticated, IsActiveUser, ]

    def get_object(self):
        """ Возвращает контакт звена сети по id звена и id контакта """

        return Contacts.objects.get(pk=self.kwargs['pk'], element_chain=self.kwargs['element_chain_id'])


class ElementChainProductsCreateAPIView(CreateAPIView):
    """ Класс-представление для создания продукта заводом """

    queryset = ElementChain.objects.all()
    serializer_class = ElementChainProductsSerializer
    permission_classes = [IsAuthenticated, IsActiveUser, ]

    class Meta:
        model = ElementChain
        fields = ('pk', 'products')


class ElementChainProductsListAPIView(ListAPIView):
    """ Класс-представление для списка звеньев цепи с их продуктами """

    queryset = ElementChain.objects.all()
    serializer_class = ElementChainProductsSerializer
    permission_classes = [IsAuthenticated, IsActiveUser, ]

    class Meta:
        model = ElementChain
        fields = ('pk', 'products')


class ElementChainProductsRetrieveAPIView(RetrieveAPIView):
    """ Класс-представление для звена цепи с продуктами по заданному pk"""

    queryset = ElementChain.objects.all()
    serializer_class = ElementChainProductsSerializer
    permission_classes = [IsAuthenticated, IsActiveUser, ]

    class Meta:
        model = ElementChain
        fields = ('pk', 'products')


class ElementChainProductsUpdateAPIView(UpdateAPIView):
    """ Класс-представление для изменения продукта заводом или добавления продукта другими звеньями цепи (не завод) """

    queryset = ElementChain.objects.all()
    serializer_class = ElementChainProductsSerializer
    http_method_names = ['patch',]
    permission_classes = [IsAuthenticated, IsActiveUser, ]

    class Meta:
        model = ElementChain
        fields = ('pk', 'products')

    def get_object(self):
        """ Возвращает звена сети по id звена """

        return ElementChain.objects.get(pk=self.kwargs['pk'])


class ProductsDestroyAPIView(DestroyAPIView):
    """ Класс-представление для удаления продукта заводом"""

    queryset = Product.objects.all()
    lookup_field = "element_chain_id"
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsActiveUser, ]

    def get_object(self):
        """ Возвращает продукт звена сети по pk звена и id контакта """

        return Product.objects.get(pk=self.kwargs['pk'])

