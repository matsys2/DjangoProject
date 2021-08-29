from django.core.exceptions import ValidationError
from django.forms import (
    ModelForm, CharField, ModelChoiceField, IntegerField, DateField, Textarea
)
from viewer.models import Movie
from viewer.validators import PastMonthField, capitalized_validator

import re


class MovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'

        title = CharField(validators=[capitalized_validator])
        rating = IntegerField(min_value=1, max_value=10)
        released = PastMonthField()

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
