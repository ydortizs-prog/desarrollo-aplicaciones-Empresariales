from django.shortcuts import get_object_or_404, render
from .models import Article, Category


def _sidebar_categories():
    """Categories shown in the sidebar on every page."""
    return Category.objects.all()


def frontpage(request):
    """Portal home with latest published articles."""
    articles = (
        Article.objects.filter(is_published=True)
        .select_related('author')
        .prefetch_related('categories')
    )
    return render(request, 'news/frontpage.html', {
        'articles': articles,
        'categories': _sidebar_categories(),
    })


def article_detail(request, pk):
    """Full article with image, author and categories."""
    article = get_object_or_404(
        Article.objects.select_related('author').prefetch_related('categories'),
        pk=pk,
        is_published=True,
    )
    return render(request, 'news/article_detail.html', {
        'article': article,
        'categories': _sidebar_categories(),
    })


def category_list(request, pk):
    """Articles of one category, reusing the card fragment."""
    category = get_object_or_404(Category, pk=pk)
    articles = (
        category.articles.filter(is_published=True)
        .select_related('author')
        .prefetch_related('categories')
    )
    return render(request, 'news/category_list.html', {
        'category': category,
        'articles': articles,
        'categories': _sidebar_categories(),
    })
