from django.shortcuts import render


def index(request):
    return render(request, template_name="main/index.html")

def about(request):
    return render(request, template_name="main/about.html")

def services(request):
    return render(request, template_name="main/services.html")

def contacts(request):
    return render(request, template_name="main/contacts.html")
