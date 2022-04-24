from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from django.http import JsonResponse, HttpResponse


from .models import Actor, Movie, Category, Genre
from .forms import ReviewForm

class GenreYear:
    """Film genres and release years"""
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year")


class MoviesView(GenreYear, ListView):
    """List of films"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)

    
		 
class MovieDetailView(GenreYear, DetailView):
    """Full movie description"""
    model = Movie
    slug_field = "url"


class AddReview(View):
    """Reviews"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())

class ActorView(GenreYear, DetailView):
    """Getting information about an actor"""
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = "name"


class FilterMoviesView(GenreYear, ListView):
    """"Movie filter"""
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) | 
            Q(genres__in=self.request.GET.getlist("genre"))
            )
        return queryset


class JsonFilterMoviesView(ListView):
    """Фильтр фильмов в json"""
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct().values("title", "tagline", "url", "poster")
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"movies": queryset}, safe=False)

   