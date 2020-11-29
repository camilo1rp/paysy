from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'start', views.StartPayment, basename='start_payment')
router.register(r'paygateway', views.PayGateWayViewSet, basename='PayGateWay')

app_name = 'payment'
urlpatterns = [
    path('', include(router.urls))
]
