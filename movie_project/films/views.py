from django.shortcuts import render, get_object_or_404, redirect
from .models import Film
from .forms import FilmForm


def films(request):
    films = Film.objects.all()
    return render(request, template_name="films/films.html", context={"films": films})


def film_detail(request, film_id):
    film = get_object_or_404(Film, id=film_id)
    return render(request, template_name="films/film_detail.html", context={"film": film})


def add_film(request):
    if request.method == 'POST':
        form = FilmForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('film_list')
    else:
        form = FilmForm()

    return render(request, 'films/add_film.html', context={'form': form})


def delete_film(request, film_id):
    film = get_object_or_404(Film, id=film_id)
    film.delete()
    return redirect('film_list')

