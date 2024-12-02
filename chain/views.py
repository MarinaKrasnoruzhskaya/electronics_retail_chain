from django.shortcuts import render
from rest_framework.generics import DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from chain.models import ElementChain, Contacts
from chain.serializers import ElementChainSerializer, ElementChainUpdateSerializer, ContactsSerializer


class ElementChainViewSet(ModelViewSet):
    """ Класс-представление для модели ElementChain """

    queryset = ElementChain.objects.all()
    serializer_class = ElementChainSerializer

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

    def get_object(self):
        """ Возвращает контакт звена сети по id звена и id контакта """

        return Contacts.objects.get(pk=self.kwargs['pk'], element_chain=self.kwargs['element_chain_id'])