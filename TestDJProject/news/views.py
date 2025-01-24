from django.shortcuts import render
from .models import NewsPost



def news(request):
    news = NewsPost.objects.all()

    return render(request, template_name="news/news.html", context={"news": news})

