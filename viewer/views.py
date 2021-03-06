from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
import datetime

from viewer.models import Movie
from viewer.forms import MovieForm

from logging import getLogger

LOGGER = getLogger()

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


@login_required
def generate_demo(request):
    our_get = request.GET.get('name', '')
    return render(
        request, template_name='demo.html',
        context={'our_get': our_get,
                 'list': ['pierwszy', 'drugi', 'trzeci', 'czwarty'],
                 'nasza_data': datetime.datetime.now()
                 }

    )

class MoviesView(ListView):
    template_name = 'movies.html'
    model = Movie


class MovieCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'formAddEditMovie.html'
    form_class = MovieForm
    # adres pobrany z URLs na ktory zostaniemy przekierowani
    # gdy walidacja sie powiedzie(movie_create pochodzi  z name!!)
    success_url = reverse_lazy('movie_create')
    permission_required = 'viewer.add_movie'

    # co ma sie dziac gdy formularz przeszedl walidacje

    # co ma sie dziac gdy formularz nie przejdzie walidacji
    def form_invalid(self, form):
        # odkladamy w logach informacje o opreacji
        LOGGER.warning('User provided invalid data')
        # zwracamy wynik dzialania pierwotnej funkcji form_ib=nvalid
        return super().form_invalid(form)


class MovieUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'formAddEditMovie.html'
    form_class = MovieForm
    # adres pobrany z URLs na ktory zostaniemy przekierowani
    # gdy walidacja sie powiedzie(movie_create pochodzi  z name!!)
    success_url = reverse_lazy('index')
    # Nazwa encji, z ktorej bedziemy kasowac rekord
    model = Movie
    permission_required = 'viewer.change_movie'

    def form_invalid(self, form):
        # odkladamy w logach informacje o opreacji
        LOGGER.warning('User provided invalid data')
        # zwracamy wynik dzialania pierwotnej funkcji form_ib=nvalid
        return super().form_invalid(form)


class MovieDeleteView(PermissionRequiredMixin, DeleteView):
    # nazwa szablonu wraz z rozszerzeniem ktora pobieramy z folderu templates
    template_name = 'delete_movie.html'
    success_url = reverse_lazy('index')
    # Nazwa encji, z ktorej bedziemy kasowac rekord
    model = Movie
    permission_required = 'viewer.delete_movie'
