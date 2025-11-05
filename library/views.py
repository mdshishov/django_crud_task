import json

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views import View

from library.models import Author


@method_decorator(require_http_methods(['GET', 'POST', 'PUT', 'DELETE']), name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AuthorView(View):
    def get(self, request: WSGIRequest, author_id: int = None):
        if author_id is None:
            authors = Author.objects.all()
            return JsonResponse({'data': [author.to_dict() for author in authors]})

        try:
            author = Author.objects.get(id=author_id)
            return JsonResponse({'data': author.to_dict()})
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
        return JsonResponse({'data': author.to_dict()})

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

        return JsonResponse({'status': 'Updated', 'author': author.to_dict()})

    def delete(self, request, author_id):
        if author_id is None:
            return JsonResponse({'error': 'Bad request'}, status=400)

        try:
            author = Author.objects.get(id=author_id)
            author_dict = author.to_dict()
            author.delete()
            return JsonResponse({'status': 'Deleted', 'item': author_dict})
        except Author.DoesNotExist:
            return JsonResponse({'error': 'Author not found'}, status=404)
