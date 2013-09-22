# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404, redirect

from articles.models import CIFArticle, CIFArticleForm

def index(request):
    form = CIFArticleForm()
    return render(request, 'articles/index.html', { 'form' : form })

def add(request):

    if not request.POST:
        return redirect("/")

    article = None

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

    if article:
        return redirect("/" + str(article.id))
    else:
        return render(request, 'articles/index.html', { 'form' : form })


def detail(request, article_id):
    article = get_object_or_404(CIFArticle, id=article_id)
    return render(request, 'articles/detail.html', {'article' : article})

