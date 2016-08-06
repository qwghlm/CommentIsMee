from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.core.cache import cache

from articles.models import CIFArticle
from .forms import CIFArticleForm

def index(request):
    """
    Handle requests to the homepage
    """
    article = None
    # If a user has submitted a URL...
    if request.POST:

        form = CIFArticleForm(request.POST)
        if (form.is_valid()):
            try:
                article = form.save(commit=False)
                existing_articles = CIFArticle.objects.filter(url=article.url).count()

                if existing_articles:
                    article = CIFArticle.objects.get(url=article.url)
                else:
                    article.measure_ego()
                    article.save()

            except ValueError, e:
                article = None
                form._errors["url"] = form.error_class([str(e)])

    # If no URL submitted, just set up a blank form
    else:
        form = CIFArticleForm()

    # If an article is found or created due to a user submission, redirect there
    if article:
        return redirect(reverse("articles:detail", args=(article.id,)))

    # Else show the homepage & rendered form
    else:

        top_articles = cache.get('cim:top_articles')
        if top_articles is None:
            top_articles = CIFArticle.objects.filter(is_cif=1).order_by('-score')[:10]
            cache.set('cim:top_articles', top_articles, 60)

        latest_articles = cache.get('cim:latest_articles')
        if latest_articles is None:
            latest_articles = CIFArticle.objects.filter(is_cif=1).order_by('-id')[:5]
            cache.set('cim:latest_articles', latest_articles, 30)

        return render(request, 'articles/index.html', {
            'form' : form ,
            'top_articles' : top_articles,
            'latest_articles' : latest_articles
        })

def detail(request, article_id):
    """
    Handle detail view for an article
    """
    # Quite simple, set up article and form
    form = CIFArticleForm()
    article_key = 'cim:article:%s' % article_id
    article = cache.get(article_key)
    if article is None:
        article = get_object_or_404(CIFArticle, id=article_id)
        cache.set(article_key, article, 300)

    return render(request, 'articles/detail.html', {
        'article' : article,
        'form' : form })
