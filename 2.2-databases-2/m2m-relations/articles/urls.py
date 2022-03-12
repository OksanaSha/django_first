from django.urls import path

from articles.views import articles_list
from django.contrib import admin

urlpatterns = [
    path('', articles_list, name='articles'),
    path('admin', admin.site.urls)
]
