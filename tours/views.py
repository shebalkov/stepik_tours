import random

from django.shortcuts import render
from django.views import View

from tours import data


class MainView(View):
    def get(self, request, *args, **kwargs):
        tours = {i: data.tours[i] for i in
                 random.sample(range(1, len(data.tours)), 6)}
        return render(request, 'index.html', context={
            'tours': tours,
            'departures': data.departures,
            'title': data.title,
            'subtitle': data.subtitle,
            'description': data.description})


class DepartureView(View):
    def get(self, request, departure, *args, **kwargs):
        chosen_tours = {key: value for (key, value) in data.tours.items()
                        if value['departure'] == departure}
        min_price = min(chosen_tours.values(),
                        key=lambda v: v['price']
                        if v['price'] != 'NaN' else float('inf'))['price']
        max_price = max(chosen_tours.values(),
                        key=lambda v: v['price']
                        if v['price'] != 'NaN' else float('inf'))['price']
        min_nights = min(chosen_tours.values(),
                         key=lambda v: v['nights']
                         if v['nights'] != 'NaN' else float('inf'))['nights']
        max_nights = max(chosen_tours.values(),
                         key=lambda v: v['nights']
                         if v['nights'] != 'NaN' else float('inf'))['nights']

        return render(request, 'departure.html', context={
            'tours': chosen_tours,
            'departure_city':
                data.departures[departure],
            'min_price': min_price,
            'max_price': max_price,
            'min_nights': min_nights,
            'max_nights': max_nights,
            'departures': data.departures,
            'title': data.title})


class TourView(View):
    def get(self, request, tour_id, *args, **kwargs):
        return render(request, 'tour.html', context={
            'title': data.title,
            'tour': data.tours[tour_id],
            'departure_city':
                data.departures[data.tours[tour_id]['departure']],
            'departures': data.departures})
