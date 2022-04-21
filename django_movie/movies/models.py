from django.urls import reverse
from datetime import date
from django.db import models


class Category(models.Model):
    """Category"""
    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Actor(models.Model):
    """Actor and directors """
    name = models.CharField("Имя", max_length=100)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="actors/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Актёры и режиссёры"
        verbose_name_plural = "Актёры и режиссёры"


class Genre(models.Model):
    """Genres"""
    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Movie(models.Model):
    """Movies"""
    title = models.CharField("название", max_length=100)
    tagline = models.CharField("Слоган", max_length=100, default='')
    description = models.TextField("Описание")
    poster = models.ImageField("Постер", upload_to='movies/')
    year = models.PositiveSmallIntegerField("Дата выхода", default=2019)
    country = models.CharField("Страна", max_length=30)
    directors = models.ManyToManyField(
        Actor, verbose_name="режиссёр", related_name='film_director')
    actors = models.ManyToManyField(
        Actor, verbose_name="акёры", related_name='film_actor')
    genres = models.ManyToManyField(Genre, verbose_name="жанры")
    world_premier = models.DateField("Примьера в мире", default=date.today)
    budget = models.PositiveSmallIntegerField(
        "Бюджет", default=0, help_text="указывать сумму в долларах")
    fees_in_usa = models.PositiveSmallIntegerField(
        "Сборы в США", default=0, help_text='указывать сумму в долларах'
    )
    fees_in_world = models.PositiveSmallIntegerField(
        "Сборы в мире", default=0, help_text='указывать сумму в долларах'
    )
    category = models.ForeignKey(
        Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True
    )
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

    
class MovieShots(models.Model):
    """Film stills"""
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to='movie_shots/')
    movie = models.ForeignKey(
        Movie, verbose_name='Фильм', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр из Фильма"
        verbose_name_plural = "Кадры из Фильма"


class RatingStar(models.Model):
    """Star rating"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звёзды рейтинга"


class Rating(models.Model):
    """Rating"""
    ip = models.CharField("IP адресс", max_length=15)
    star = models.ForeignKey(
        RatingStar, on_delete=models.CASCADE, verbose_name='звезда')
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, verbose_name="фильм")

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
    """Reviews"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    movie = models.ForeignKey(
        Movie, verbose_name="фильм", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
