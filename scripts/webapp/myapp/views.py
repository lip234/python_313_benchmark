from django.shortcuts import render

from .models import Article


# Create your views here.

def index(request):
    return render(request, 'index.html')


def article(request, article_id):
    article = Article.objects.get(pk=article_id)
    return render(request, 'article.html', {'article': article})
