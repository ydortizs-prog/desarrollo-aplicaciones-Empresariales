from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.frontpage, name='frontpage'),
    path('article/<int:pk>/', views.article_detail, name='article-detail'),
    path('category/<int:pk>/', views.category_list, name='category-list'),
]
