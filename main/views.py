from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MovieSerializers, MovieDetailSerializers, MovieCreateSerializer
from .models import Movie


@api_view(['GET'])
def index(request):
    context = {
        'number': 100,
        'float': 1.11,
        'text': 'Hello world',
        'list': [1, 3, 2],
        'dict': {'name': 'Aziz'}
    }
    return Response(data=context, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def movie_list_view(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        data = MovieSerializers(movies, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        print('request.data -', request.data)
        serializer = MovieSerializers(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={'errors': serializer.errors})
        name = request.data['name']
        description = request.data.get('description', '')
        duration = request.data['duration']
        is_active = request.data['is_active']
        genres = request.data['genres']
        movie = Movie.objects.create(
            name=name, description=description, duration=duration,
            is_active=is_active
        )
        movie.genres.set(genres)
        return Response(data=MovieSerializers(movie).data,
                        status=status.HTTP_201_CREATED)


@api_view(['GET'])
def movie_detail_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Movie not found!'})
    data = MovieDetailSerializers(movie, many=False).data
    return Response(data=data)