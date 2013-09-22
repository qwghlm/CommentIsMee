# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse

from articles.models import CIFArticle, CIFArticleForm

def index(request):

    article = None
    if request.POST:
        try:
            article = CIFArticle.objects.get(url=request.POST.get('url'))

        except CIFArticle.DoesNotExist:
            form = CIFArticleForm(request.POST)

            # FIXME - incorporate updating & validation into Django's own validation?
            if (form.is_valid()):            
                try:
                    article = form.save(commit=False)
                    article.measure_ego()
                    article.save()
                except ValueError:
                    article = None
    else:
        form = CIFArticleForm()

    if article:
        return redirect(reverse("articles:detail", args=(article.id,)))

    else:
        top_articles = CIFArticle.objects.order_by('-score')[:5]
        return render(request, 'articles/index.html', {
            'form' : form ,
            'top_articles' : top_articles
        })

def detail(request, article_id):
    article = get_object_or_404(CIFArticle, id=article_id) # TODO What does the 404 look like?
    return render(request, 'articles/detail.html', {'article' : article})

