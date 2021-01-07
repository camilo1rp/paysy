from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'zpstart', views.ZPStartPayment, basename='start_payment')
router.register(r'paygateway', views.PayGateWayViewSet, basename='PayGateWay')
router.register(r'zpconfirm', views.ZonaPagosConfirmView, basename='zpConfirm')
router.register(r'transtatus', views.TransactionStatusView,
                basename='transtatus')
router.register(r'customerDetails', views.CustomerDetailView,
                basename='customerDetails')

app_name = 'payment'
urlpatterns = [
    path('', include(router.urls)),
    path('zonapagos/test', views.ZonaPagosTest.as_view(), name='zp-test'),
    path('zonapagos/list', views.ZonaPagosList.as_view(), name='zp-list')
]
