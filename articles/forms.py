from django.forms import ModelForm, TextInput, URLField
from .models import CIFArticle

class CIFArticleForm(ModelForm):
    """
    Simplified URL-only form for user to search for
    """
    attrs = {
        'class' : 'span7',
        'placeholder' : 'Type or paste a CIF link here'
    }
    url = URLField(widget=TextInput(attrs=attrs))
    class Meta:
        model = CIFArticle
        fields = ['url']

