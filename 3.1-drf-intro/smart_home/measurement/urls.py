from django.urls import path

from .views import SensorCreateAPIView, SensorUpdateAPIView, MeasurementCreateAPIView

urlpatterns = [
    path('sensors/', SensorCreateAPIView.as_view(), name='create_sensor'),
    path('sensors/<int:pk>', SensorUpdateAPIView.as_view(), name='update_sensor'),
    path('measurements/', MeasurementCreateAPIView.as_view(), name='add_measurement'),
]
