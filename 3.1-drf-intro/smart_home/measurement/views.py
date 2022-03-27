from django.forms import model_to_dict
from rest_framework import generics
from rest_framework.response import Response

from .models import Measurement, Sensor
from .serializers import SensorSerializer, MeasurementSerializer, SensorDetailSerializer


class SensorCreateAPIView(generics.ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SensorUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class MeasurementCreateAPIView(generics.ListCreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)