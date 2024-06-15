from django.urls import path
from . import views
app_name = 'myapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('articles/<int:article_id>', views.article, name='article'),
]