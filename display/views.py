from django.shortcuts import render
import numpy as np
from random import sample
from .models import Everything
from display.recommender import recommend

try:
    if similarity:
        pass
except NameError:
    similarity = np.load('D:\\Documents\\Python\\movieRec\\similarity.npy')


# Create your views here.
def homepage_view(request, *args, **kwargs):
    return render(request, "home.html", {})


def search_view(request, *args, **kwargs):
    data = None
    search_quer = None
    if request.method == 'POST':
        if request.POST['submit'] == 'Random':
            data = sample(list(Everything.objects.all()), 50)
            search_quer = "Random Search"
        elif request.POST['search'] == '':
            search_quer = "Random Search"
            data = sample(list(Everything.objects.all()), 50)
        else:
            search_quer = "Search result for " + request.POST['search']
            data = Everything.objects.all().filter(title__icontains=request.POST['search'])
    return render(request, "search.html", {'data': data, 'search': search_quer})


def output_view(request, db_id, *args, **kwargs):
    data = Everything.objects.all().filter(imdb_id=db_id)
    dat = [j for i in data.values_list() for j in i]
    col = ['IMDB_ID', 'Title', 'isMovie', 'Genre', 'Actors', 'Directors', 'Plot',
           'Date_Published', 'Keywords', 'Ratings', 'External_Links', 'TMDB_ID',
           'TMDB_Rating', 'TMDB_Rating_Count', 'Image_URL', 'Number_of_Ratings']
    searched_entry = {col[i]: dat[i] for i in range(len(dat))}
    lst = recommend(searched_entry['Title'], similarity)
    recommendations = {i: {'title': v[0], 'image': v[1], 'id': v[2]} for i, v in enumerate(lst)}
    searched_entry['External_Links'] = searched_entry['External_Links'].split(',')
    searched_entry['isMovie'] = 'movie' if searched_entry['isMovie'] else 'tv'
    return render(request, "result.html", {'searched_entry': searched_entry, 'recommendations': recommendations})
