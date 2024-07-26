from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from django.core.cache import cache

from .models import Book
from .forms import BookCreateForm, BookEditForm, BookSearchForm

import logging

logger = logging.getLogger(__name__)


def delete_cache_keys():
    key_list = ['cached_book_list']
    for col in ('pk', 'title', 'author', 'year', 'read'):
        key_list += ['cached_book_list_sorted_' + col]
        key_list += ['cached_book_list_sorted_-' + col]
    cache.delete_many(key_list)

    logger.debug(f"Deleted cache keys: {key_list}")


@require_http_methods(['GET'])
def book_list(request):
    query = request.GET.get('search_query', '')
    if query:
        # Выполняем поиск и возвращаем результаты
        return search_books(request, query)

    # Кэширование списка книг
    book_list = cache.get_or_set('cached_book_list', Book.objects.all())
    form = BookCreateForm(auto_id=False)
    logger.debug('Book list retrieved from cache')
    return render(request, 'base.html', {'book_list': book_list, 'form': form})


@require_http_methods(['POST'])
def create_book(request):
    form = BookCreateForm(request.POST)
    if form.is_valid:
        book = form.save()
        delete_cache_keys()
        logger.debug(f"Book {book.pk} created and cache keys deleted")
    return render(request, 'partial_book_detail.html', {'book': book})


def update_book_details(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        form = BookEditForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            delete_cache_keys()
            return render(request, 'partial_book_detail.html', {'book': book})
    else:
        form = BookEditForm(instance=book)
    return render(request, 'partial_book_update_form.html', {'book': book, 'form': form})


@require_http_methods(["GET"])
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'partial_book_detail.html', {'book': book})


@require_http_methods(['DELETE'])
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    delete_cache_keys()
    return HttpResponse()


@require_http_methods(['PATCH'])
def update_book_status(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.read:
        book.read = False
    else:
        book.read = True
    book.save()
    delete_cache_keys()
    return render(request, 'partial_book_detail.html', {'book': book})


@require_http_methods(['GET'])
def book_list_sort(request, filter, direction):
    filter_dict = {_('id'): 'pk',
                   _('title'): 'title',
                   _('author'): 'author',
                   _('year'): 'year',
                   _('read'): 'read'}

    if filter in filter_dict:
        sort_str = ('-', '')[direction == _('ascend')] + filter_dict[filter]
        cache_key = 'cached_book_list_sorted_' + sort_str
        book_list = cache.get_or_set(
            cache_key, Book.objects.order_by(sort_str))
    else:
        book_list = cache.get_or_set('cached_book_list', Book.objects.all())
    logger.debug(
        f"Book list sorted by {filter} in {direction} order and cached"
    )
    return render(request, 'partial_book_list.html', {'book_list': book_list})


def search_books(request, query):
    form = BookSearchForm(request.GET or None)
    results = Book.objects.filter(
        Q(title__icontains=query) |
        Q(author__icontains=query) |
        Q(year__icontains=query)
    )
    return render(request, 'base.html', {'book_list': results, 'form': form})
