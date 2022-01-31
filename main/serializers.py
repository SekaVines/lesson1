from rest_framework import serializers
from .models import Movie, Genre, Rating


class GenreSerializers(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class RatingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = 'id text value'.split()


class MovieSerializers(serializers.ModelSerializer):
    # genres = GenreSerializers(many=True)
    ratings = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        # fields = '__all__'
        # fields = 'id name'.split()
        fields = ['id', 'name', 'genres', 'ratings', 'count_genres']

    def get_ratings(self, movie):
        rate = Rating.objects.filter(movie=movie, value__gt=3)
        data = RatingSerializers(rate, many=True).data
        return data

    def get_genres(self, movie):
        return GenreSerializers(movie.genres.filter(is_active=True), many=True).data


class MovieDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name', 'description', 'duration', 'count_genres']


from rest_framework.exceptions import ValidationError


class MovieCreateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=3, max_length=10)
    description = serializers.CharField(required=True)
    duration = serializers.IntegerField(default=0)
    is_active = serializers.BooleanField()
    genres = serializers.ListField(child=serializers.IntegerField())

    def validate_name(self, name):
        movies = Movie.objects.filter(name=name)
        if movies:
            raise ValidationError('Movie already exists!')
        return name

    def validate(self, attrs):
        name = attrs['name']
        if movies:
            raise ValidationError('Movie already exists!')
        return name
