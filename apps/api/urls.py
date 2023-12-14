from rest_framework import routers
from .views import PaymentViewSet

router = routers.SimpleRouter()
router.register(r'webhook-pagseguro', PaymentViewSet, basename='s')

urlpatterns = [] + router.urls