from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpRequest
from django.utils.timezone import now
from .models import Post, Category


def index(request: HttpRequest):
    """
    Отображает главную страницу блога
    со списком 5 последних публикаций.
    """
    posts = Post.objects.select_related(
        'author', 'category', 'location',
    ).filter(
        is_published=True,
        pub_date__lte=now(),
        category__is_published=True
    ).order_by('-pub_date')[:5]
    return render(request, 'blog/index.html', {'post_list': posts})


def post_detail(request: HttpRequest, id: int):
    """Отображает полный текст выбранного поста."""
    post = get_object_or_404(
        Post.objects.select_related(
            'author', 'category', 'location',
        ).filter(
            is_published=True,
            pub_date__lte=now(),
            category__is_published=True
        ),
        pk=id
    )
    return render(request, 'blog/detail.html', context={'post': post})


def category_posts(request: HttpRequest, category_slug: str):
    """Отображает поcты выбранной категории."""
    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=category_slug
    )
    posts = Post.objects.select_related(
        'author', 'category', 'location',
    ).filter(
        is_published=True,
        pub_date__lte=now(),
        category=category,
        category__is_published=True
    ).order_by('-pub_date')
    return render(
        request, 'blog/category.html',
        {'category': category, 'post_list': posts}
    )
