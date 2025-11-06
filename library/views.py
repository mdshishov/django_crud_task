import json

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views import View

from library.models import Author, Book, Genre


@require_http_methods(['GET'])
def index(request):
    return redirect('book_list')


@require_http_methods(['GET'])
@csrf_exempt
def book_edit(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        return JsonResponse({'status': 'Success!'})
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)


@method_decorator(require_http_methods(['GET', 'POST', 'DELETE']), name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class BookView(View):
    def get(self, request: WSGIRequest, book_id: int = None):
        if book_id is None:
            books = Book.objects.all()
            book_list = [{
                'id': book.pk,
                'title': book.title,
                'author': book.author.full_name(),
            } for book in books]
            return render(
                request,
                template_name='book_list.html',
                context={
                    'book_list': book_list,
                },
            )

        try:
            book = Book.objects.get(id=book_id)
            book_dict = {
                'id': book.pk,
                'title': book.title,
                'isbn': book.isbn,
                'author': book.author.full_name(),
                'co_authors': ', '.join([co_author.full_name() for co_author in book.co_authors.all()]),
                'genres': ', '.join([genre.name for genre in book.genres.all()]),
                'publication_year': book.publication_year,
                'summary': book.summary,
            }
            return render(
                request,
                template_name='book_detail.html',
                context={'book': book_dict},
            )
        except Book.DoesNotExist:
            return JsonResponse({'error': 'Book not found'}, status=404)


@method_decorator(require_http_methods(['GET', 'POST']), name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class BookNewView(View):
    pass


@method_decorator(require_http_methods(['GET', 'POST', 'PUT', 'DELETE']), name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AuthorView(View):
    def get(self, request: WSGIRequest, author_id: int = None):
        if author_id is None:
            authors = Author.objects.all()
            return JsonResponse(
                {'data': [author.to_dict() for author in authors]},
                json_dumps_params={'ensure_ascii': False},
            )

        try:
            author = Author.objects.get(id=author_id)
            return JsonResponse(
                {'data': author.to_dict()},
                json_dumps_params={'ensure_ascii': False},
            )
        except Author.DoesNotExist:
            return JsonResponse({'error': 'Author not found'}, status=404)

    def post(self, request: WSGIRequest, author_id: int = None):
        if author_id is not None:
            return JsonResponse({'error': 'Bad request'}, status=400)
        try:
            data = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'error': 'Wrong JSON'}, status=400)

        if 'first_name' not in data or 'last_name' not in data:
            return JsonResponse({'error': 'First and last name are required'}, status=400)

        author = Author(**data)
        author.save()
        return JsonResponse(
            {'data': author.to_dict()},
            json_dumps_params={'ensure_ascii': False},
        )

    def put(self, request: WSGIRequest, author_id: int = None):
        if author_id is None:
            return JsonResponse({'error': 'Bad request'}, status=400)

        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return JsonResponse({'error': 'Author not found'}, status=404)

        try:
            data = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'error': 'Wrong JSON'}, status=400)

        author.first_name = data.get('first_name')
        author.last_name = data.get('last_name')
        author.bio = data.get('bio')
        author.birth_date = data.get('birth_date')
        author.save()

        return JsonResponse(
            {'status': 'Updated', 'author': author.to_dict()},
            json_dumps_params={'ensure_ascii': False},
        )

    def delete(self, request, author_id):
        if author_id is None:
            return JsonResponse({'error': 'Bad request'}, status=400)

        try:
            author = Author.objects.get(id=author_id)
            author_dict = author.to_dict()
            author.delete()
            return JsonResponse(
                {'status': 'Deleted', 'item': author_dict},
                json_dumps_params={'ensure_ascii': False},
            )
        except Author.DoesNotExist:
            return JsonResponse({'error': 'Author not found'}, status=404)
