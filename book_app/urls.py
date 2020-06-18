from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create_user', views.create_user),
    path('success', views.success),
    path('login', views.login),
    path('create_book', views.create_book),
    path('books/<int:id>', views.one_book),
    path('like/<int:book_id>', views.create_like),
    path('unlike/<int:book_id>', views.delete_like),
    path('log_out', views.log_out),
]