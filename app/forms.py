from typing import List

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import BigAutoField

std_widget = forms.TextInput(attrs={'autocomplete': 'off'})


class NewUserForm(UserCreationForm):
    id = BigAutoField(primary_key=True)

    class Meta:
        model = User
        fields = ("username", "password1")



class ScenarioNameForm(forms.Form):
    name = forms.CharField(max_length=32, label='Scenario Name', widget=std_widget)


class ScenarioEditForm(forms.Form):
    name = forms.CharField(max_length=32, label='Scenario Name', widget=std_widget)
    tasks = forms.IntegerField(min_value=0, label="Number of Tasks", widget=std_widget)
    budget = forms.DecimalField(min_value=0, label="Budget €", decimal_places=2, widget=std_widget)


class TextBlockForm(forms.Form):
    header = forms.CharField(max_length=32, label='Header', widget=std_widget)
    content = forms.CharField(max_length=2048, label="Content")


class DecisionEditForm(forms.Form):
    continue_text = forms.CharField(max_length=32, label="Continue Button Text", widget=std_widget)
    text = List[TextBlockForm]


class AnswerForm(forms.Form):
    text = forms.CharField(max_length=32)
    points = forms.IntegerField(min_value=0, max_value=1000)
