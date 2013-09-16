# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404

from articles.models import CIFArticle

def index(request):
	return render(request, 'articles/index.html', {})

def add(request):
	return HttpResponse("Hello world, adding...")

def detail(request, article_id):
	article = get_object_or_404(CIFArticle, id=article_id)
	return render(request, 'articles/detail.html', {'article' : article})

