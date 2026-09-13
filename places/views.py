import random

from django.http import Http404
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import PlaceForm

SESSION_KEY = 'places'

DEFAULT_PLACES = [
    {
        'name': 'Coffee Boss',
        'place_type': 'кафе',
        'location': 'Чернігів',
        'rating': 5,
        'description': (
            'Найсмачніша кава в місті, ціни не київські. Мережа з багатьма '
            'точками по Чернігову. Якщо будете в Чернігові — обов\'язково '
            'завітайте.'
        ),
    },
    {
        'name': 'Musafir Podil',
        'place_type': 'кримськотатарський заклад',
        'location': 'вул. Притисько-Микільська, 2, Київ, Україна, 04071',
        'rating': 5,
        'description': (
            'Кримськотатарська кухня, великий вибір страв, готують дуже '
            'смачно. Чудове місце.'
        ),
    },
    {
        'name': "McDonald's",
        'place_type': 'фастфуд',
        'location': 'Київ',
        'rating': 3,
        'description': (
            'Мережа фастфуду, багато точок по Україні, але найбільше люблю '
            'київський. Беру там тільки чікен рол.'
        ),
    },
    {
        'name': 'Рідні двори на Троєщині',
        'place_type': 'прогулянка',
        'location': 'Троєщина, Київ',
        'rating': 5,
        'description': (
            'Жила тут перші 2 курси університету в гуртожитку НаУКМА, який '
            'зараз на ремонті, але вулиця і місця рідні.'
        ),
    },
]


def _stars(rating):
    rating = int(rating)
    return '★' * rating + '☆' * (5 - rating)


def _seed_place(place, place_id):
    seeded = dict(place)
    seeded['id'] = place_id
    seeded['created'] = timezone.localdate().isoformat()
    return seeded


def get_places(request):
    if SESSION_KEY not in request.session:
        request.session[SESSION_KEY] = [
            _seed_place(place, index + 1)
            for index, place in enumerate(DEFAULT_PLACES)
        ]
    return request.session[SESSION_KEY]


def add_place(request, cleaned_data):
    places = get_places(request)
    next_id = max((place['id'] for place in places), default=0) + 1
    new_place = _seed_place(cleaned_data, next_id)
    request.session[SESSION_KEY] = places + [new_place]


def for_display(place):
    display = dict(place)
    display['stars'] = _stars(place['rating'])
    return display


def home(request):
    places = get_places(request)
    featured = None
    if request.method == 'POST' and places:
        chosen = random.choices(
            places,
            weights=[place['rating'] for place in places],
            k=1,
        )[0]
        featured = for_display(chosen)

    context = {'featured': featured}
    return render(request, 'places/home.html', context)


def place_list(request):
    places = [for_display(place) for place in get_places(request)]
    context = {'places': places}
    return render(request, 'places/place_list.html', context)


def place_detail(request, place_id):
    places = get_places(request)
    place = next((item for item in places if item['id'] == place_id), None)
    if place is None:
        raise Http404('Місце не знайдено.')

    context = {'place': for_display(place)}
    return render(request, 'places/place_detail.html', context)


def place_add(request):
    if request.method == 'POST':
        form = PlaceForm(request.POST)
        if form.is_valid():
            add_place(request, form.cleaned_data)
            return redirect('places:place_list')
    else:
        form = PlaceForm()

    context = {'form': form}
    return render(request, 'places/place_form.html', context)
