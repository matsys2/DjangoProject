from django.core.exceptions import ValidationError
from django.forms import (
    Form, CharField, ModelChoiceField, IntegerField, DateField, Textarea
)
from viewer.models import Genre
from viewer.validators import PastMonthField

import re


class MovieForm(Form):
    title = CharField(max_length=128)  # input - max: 128
    genre = ModelChoiceField(queryset=Genre.objects)  # select -> options (pojedynczy wiersz z Genre)
    rating = IntegerField(min_value=1, max_value=10)  # input type: number, min=1, max=10
    released = PastMonthField()  # input type: date
    description = CharField(widget=Textarea, required=False)  # nie bedzie wymagane

    def clean_description(self):
        initial = self.cleaned_data['description']
        # podzial tekstu na czesci od kropki do kropki - na zdania
        sentences = re.sub(r'\s*.\s*', '.', initial).split('.')
        # zamiana na wielka litere pierwszej litery kazdego ze zdan
        # dodanie kropki powtorzenie operacji dla kolejnego zdania
        return '. '.join(sentence.capitalize() for sentence in sentences)

    def clean(self):
        result = super().clean()
        if result['genre'].name == 'comedy' and result['rating'] > 7:
            self.add_error('genre', '')
            #oznaczenie pola jako bledne bez komentarza
            self.add_error('rating', '')
            #rzucamy ogolny blad wyjatek
            raise ValidationError(
                'Commedies aren\'t so good to be over 7'
            )
        return result
