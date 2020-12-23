from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'start', views.StartPayment, basename='start_payment')
router.register(r'paygateway', views.PayGateWayViewSet, basename='PayGateWay')
router.register(r'zpconfirm', views.ZonaPagosConfirmView, basename='zpConfirm')

app_name = 'payment'
urlpatterns = [
    path('', include(router.urls)),
    path('zonapagos/test', views.ZonaPagosTest.as_view(), name='zp-test'),
    path('zonapagos/list', views.ZonaPagosList.as_view(), name='zp-list')
]
