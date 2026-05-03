from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.signup_view, name='signup'),
    path('book/', views.listBookView.as_view(),name='list-book'),
    path('book/detail/<int:pk>/', views.DetailBookView.as_view(),name='detail-book'),
    path('book/create/', views.CreateBookView.as_view(),name='create-book'),
    path('book/delete/<int:pk>/', views.DeleteBookView.as_view(),name='delete-book'),
    path('book/update/<int:pk>/', views.UpdateBookView.as_view(),name='update-book'),
    # path('logout/', views.logout_view, name='logout'),
    path('book/<int:book_id>/review/', views.CreateReviewView.as_view(), name='review'),
]
