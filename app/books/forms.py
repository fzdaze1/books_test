from django.forms import ModelForm, CharField, TextInput
from .models import Book
from django import forms
from django.utils.translation import gettext_lazy as _


class BookCreateForm(ModelForm):
    title = CharField(label='qwerty', required=True, widget=TextInput(
        attrs={"class": "clrtxt", "placeholder": _("Title")}))
    author = CharField(required=True, widget=TextInput(
        attrs={"class": "clrtxt", "placeholder": _("Author")}))
    year = CharField(required=True, widget=TextInput(
        attrs={"class": "clrtxt", "placeholder": _("Year")}))

    class Meta:
        model = Book
        fields = ['title', 'author', 'year']


class BookEditForm(BookCreateForm):
    title = CharField(required=False, widget=TextInput(
        attrs={"class": "form-control-sm form-control"}))
    author = CharField(required=False, widget=TextInput(
        attrs={"class": "form-control-sm form-control"}))
    year = CharField(required=False, widget=TextInput(
        attrs={"class": "form-control-sm form-control"}))


class BookSearchForm(forms.Form):
    search_query = forms.CharField(
        required=False,
        label=_('Search'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Введите название, автора или цену')
        })
    )
