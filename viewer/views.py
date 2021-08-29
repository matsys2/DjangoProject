from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
# Create your views here.

from viewer.models import Movie


class MoviesView(TemplateView):
    template_name = 'movies.html'
    extra_context = { 'movies': Movie.objects.all() }