import csv

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

from pagination.settings import BUS_STATION_CSV

def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    page = int(request.GET.get('page', 1))
    with open(BUS_STATION_CSV) as file:
        reader = csv.DictReader(file)
        stations = [row for row in reader]
        paginator = Paginator(stations, 10)
        bus_stations = paginator.get_page(page)

    context = {
        'bus_stations': bus_stations.object_list,
        'page': bus_stations,
    }
    return render(request, 'stations/index.html', context)
