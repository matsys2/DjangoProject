from django.shortcuts import render
from django.views.generic import ListView

# Create your views here.

from viewer.models import Movie


class MoviesView(ListView):
    template_name = 'movies.html'
    model = Movie
