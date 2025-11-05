from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(null=True)
    birth_date = models.DateField(null=True)

    def to_dict(self):
        return {
            'id': self.pk,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'bio': self.bio,
            'birth_date': self.birth_date,
        }


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True)


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    isbn = models.CharField(max_length=20, unique=True)
    publication_year = models.IntegerField()
    genres = models.ManyToManyField(Genre)
    summary = models.TextField(null=True)
