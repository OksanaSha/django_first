from django.shortcuts import render, redirect

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    sort = request.GET.get('sort')
    phones = Phone.objects.all()
    if sort == 'max_price':
        phones = sorted(phones, key=lambda x: x.price, reverse=True)
    elif sort == 'min_price':
        phones = sorted(phones, key=lambda x: x.price)
    elif sort == 'name':
        phones = sorted(phones, key=lambda x: x.name)
    context = {'phones': phones}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    context = {'phone': Phone.objects.get(slug=slug)}
    return render(request, template, context)
