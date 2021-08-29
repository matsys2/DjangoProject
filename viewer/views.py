from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView

from viewer.models import Movie
from viewer.forms import MovieForm

from logging import getLogger

LOGGER = getLogger()


class MoviesView(ListView):
    template_name = 'movies.html'
    model = Movie


class MovieCreateView(FormView):
    template_name = 'form.html'
    form_class = MovieForm
    # adres pobrany z URLs na ktory zostaniemy przekierowani
    # gdy walidacja sie powiedzie(movie_create pochodzi  z name!!)
    success_url = reverse_lazy('movie_create')

    # co ma sie dziac gdy formularz przeszedl walidacje
    def form_valid(self, form):
        # wywolanie metody form_valid z klasy nadrzednej (FormView)
        # bedziemy zwracac wynik z niej uzyskany
        result = super().form_valid(form)
        # w obiekcie cleaned_data przechowujemy wynik dzialania
        # funkcji "czyszczacych"
        cleaned_data = form.cleaned_data
        # zapisujemy do bazy nowy film:
        Movie.objects.create(
            title=cleaned_data['title'],
            genre=cleaned_data['genre'],
            rating=cleaned_data['rating'],
            released=cleaned_data['released'],
            description=cleaned_data['description'],
        )
        return result
        # Zwracamy result - patrz komentarz nad form_valid

    # co ma sie dziac gdy formularz nie przejdzie walidacji
    def form_invalid(self, form):
        # odkladamy w logach informacje o opreacji
        LOGGER.warning('User provided invalid data')
        # zwracamy wynik dzialania pierwotnej funkcji form_ib=nvalid
        return super().form_invalid(form)
