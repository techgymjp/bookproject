from django.core.paginator import Paginator
from .consts import ITEM_PER_PAGE


from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
    )
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Avg
from .models import Book, Review

class listBookView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'book/book_list.html'
    paginate_by = ITEM_PER_PAGE

class DetailBookView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'book/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(book=self.object)
        return context

class CreateBookView(LoginRequiredMixin, CreateView):
    model = Book
    template_name = 'book/book_create.html'
    fields = ['title', 'text', 'category', 'thumbnail']
    success_url = reverse_lazy('list-book')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class DeleteBookView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'book/book_confirm.html'
    success_url = reverse_lazy('list-book')

    def get_object(self, queryset=None):
        book = super().get_object(queryset)
        if book.user != self.request.user:
            raise PermissionDenied
        return book



class UpdateBookView(LoginRequiredMixin, UpdateView):
    model = Book
    template_name = 'book/book_update.html'
    fields = ['title', 'text', 'category', 'thumbnail']
    # success_url = reverse_lazy('list-book')

    def get_object(self, queryset=None):
        book = super().get_object(queryset)
        if book.user != self.request.user:
            raise PermissionDenied
        return book

    def get_success_url(self):
        return reverse('detail-book', kwargs={'pk': self.object.id})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'book/signup.html', {'form': form})

def index_view(request):    
    # print('index_view is called')
    object_list = Book.objects.order_by('-id')
    ranking_list = Book.objects.annotate(average_rate=Avg('review__rate')).order_by('-average_rate')
    
    paginator = Paginator(object_list, ITEM_PER_PAGE)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.page(page_number)

    ranking_paginator = Paginator(ranking_list, 2)
    ranking_page_number = request.GET.get('ranking_page', 1)
    ranking_page_obj = ranking_paginator.page(ranking_page_number)

    return render(request, 'book/index.html',
                  {'page_obj': page_obj,
                   'ranking_page_obj': ranking_page_obj})

    
#def logout_view(request):
#    logout(request)
#    return redirect('index')

class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'book/review_form.html'
    fields = ['title', 'text', 'rate']
    success_url = reverse_lazy('list-book')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = Book.objects.get(pk=self.kwargs['book_id'])
        context['rate_range'] = range(1, 6)
        # print(context)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.book = get_object_or_404(Book, pk=self.kwargs['book_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail-book', kwargs={'pk': self.kwargs['book_id']})
