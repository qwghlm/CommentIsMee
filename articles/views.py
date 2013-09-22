from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse

from articles.models import CIFArticle, CIFArticleForm

def index(request):
    """
    Handle requests to the homepage
    """
    article = None
    # If a user has submitted a URL...
    if request.POST:

        # See if URL already exists in the system
        try:
            article = CIFArticle.objects.get(url=request.POST.get('url'))

        # If not, add an article in, and fetch the details from it
        except CIFArticle.DoesNotExist:
            form = CIFArticleForm(request.POST)
            if (form.is_valid()):            
                try:
                    article = form.save(commit=False)
                    article.measure_ego()
                    article.save()
                # If something goes wrong, report the error back to the user
                except ValueError, e:
                    article = None
                    form._errors["url"] = form.error_class([str(e)])

    # Else if no URL submitted, just set up a blank form
    else:
        form = CIFArticleForm()

    # If an article is found or created due to a user submission, redirect there
    if article:
        return redirect(reverse("articles:detail", args=(article.id,)))

    # Else show the homepage & rendered form
    else:
        top_articles = CIFArticle.objects.order_by('-score')[:5]
        return render(request, 'articles/index.html', {
            'form' : form ,
            'top_articles' : top_articles
        })

def detail(request, article_id):
    """
    Handle detail view for an article
    """
    # Quite simple, set up article and form
    form = CIFArticleForm()
    article = get_object_or_404(CIFArticle, id=article_id)
    return render(request, 'articles/detail.html', {
        'article' : article,
        'form' : form })
