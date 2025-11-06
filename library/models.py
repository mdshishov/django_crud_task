from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(null=True)
    birth_date = models.DateField(null=True)

    def full_name(self):
        return self.first_name + ' ' + self.last_name

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

    def to_dict(self):
        return {
            'id': self.pk,
            'name': self.name,
            'description': self.description,
        }


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    isbn = models.CharField(max_length=20, unique=True)
    publication_year = models.IntegerField()
    genres = models.ManyToManyField(Genre)
    co_authors = models.ManyToManyField(Author, blank=True, related_name='co_authors')
    summary = models.TextField(null=True)

    def to_dict(self):
        return {
            'id': self.pk,
            'title': self.title,
            'author': self.author.to_dict(),
            'isbn': self.isbn,
            'publication_year': self.publication_year,
            'genres': [genre.to_dict() for genre in self.genres.all()],
            'co_authors': [author.to_dict() for author in self.co_authors.all()],
            'summary': self.summary,
        }
