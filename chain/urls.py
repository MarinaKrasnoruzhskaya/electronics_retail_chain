from django.urls import path
from rest_framework.routers import SimpleRouter

from chain.apps import ChainConfig
from chain.views import ElementChainViewSet, ContactsDestroyAPIView

app_name = ChainConfig.name

router = SimpleRouter()
router.register("", ElementChainViewSet)

urlpatterns = [
    path('<int:element_chain_id>/contact/<int:pk>/delete/', ContactsDestroyAPIView.as_view(), name='contact-delete'),
]

urlpatterns += router.urls
