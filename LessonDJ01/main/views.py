from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("<h1>Мой проект на джанго</h1>")


def data(request):
    return HttpResponse("<h1>Страница ДАТА</h1>")

def test(request):
    return HttpResponse("<h1>Страница ТЕСТ</h1>")
