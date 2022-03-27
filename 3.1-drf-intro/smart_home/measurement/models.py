from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.pk} - {self.name}'


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')
    temperature = models.FloatField()
    date = models.DateField(auto_now=True)
    image = models.ImageField(null=True, upload_to='media')

    def __str__(self):
        return f'{self.sensor} - {self.temperature}'