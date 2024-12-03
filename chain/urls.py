from django.urls import path
from rest_framework.routers import SimpleRouter

from chain.apps import ChainConfig
from chain.views import ElementChainViewSet, ContactsDestroyAPIView, ElementChainProductsCreateAPIView, \
    ElementChainProductsListAPIView, ElementChainProductsRetrieveAPIView, ElementChainProductsUpdateAPIView, \
    ProductsDestroyAPIView

app_name = ChainConfig.name

router = SimpleRouter()
router.register("", ElementChainViewSet)

urlpatterns = [
    path('<int:element_chain_id>/contact/<int:pk>/delete/', ContactsDestroyAPIView.as_view(), name='contact-delete'),
    path('products/create/', ElementChainProductsCreateAPIView.as_view(), name='products-create'),
    path('products/', ElementChainProductsListAPIView.as_view(), name='products-list'),
    path('products/<int:pk>/', ElementChainProductsRetrieveAPIView.as_view(), name='products-detail'),
    path('products/<int:pk>/update/', ElementChainProductsUpdateAPIView.as_view(), name='products-update'),
    path('<int:element_chain_id>/products/<int:pk>/delete/', ProductsDestroyAPIView.as_view(), name='products-delete'),
]

urlpatterns += router.urls
