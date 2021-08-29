from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from viewer.models import Movie
from viewer.forms import MovieForm

from logging import getLogger

LOGGER = getLogger()


class MoviesView(ListView):
    template_name = 'movies.html'
    model = Movie


class MovieCreateView(CreateView):
    template_name = 'form.html'
    form_class = MovieForm
    # adres pobrany z URLs na ktory zostaniemy przekierowani
    # gdy walidacja sie powiedzie(movie_create pochodzi  z name!!)
    success_url = reverse_lazy('movie_create')

    # co ma sie dziac gdy formularz przeszedl walidacje

    # co ma sie dziac gdy formularz nie przejdzie walidacji
    def form_invalid(self, form):
        # odkladamy w logach informacje o opreacji
        LOGGER.warning('User provided invalid data')
        # zwracamy wynik dzialania pierwotnej funkcji form_ib=nvalid
        return super().form_invalid(form)


class MovieUpdateView(UpdateView):
    template_name = 'form.html'
    form_class = MovieForm
    # adres pobrany z URLs na ktory zostaniemy przekierowani
    # gdy walidacja sie powiedzie(movie_create pochodzi  z name!!)
    success_url = reverse_lazy('index')
    # Nazwa encji, z ktorej bedziemy kasowac rekord
    model = Movie

    def form_invalid(self, form):
        # odkladamy w logach informacje o opreacji
        LOGGER.warning('User provided invalid data')
        # zwracamy wynik dzialania pierwotnej funkcji form_ib=nvalid
        return super().form_invalid(form)


class MovieDeleteView(DeleteView):
    # nazwa szablonu wraz z rozszerzeniem ktora pobieramy z folderu templates
    template_name = 'delete_movie.html'
    success_url = reverse_lazy('index')
    # Nazwa encji, z ktorej bedziemy kasowac rekord
    model = Movie
