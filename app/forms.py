from django import forms


class ScenarioNameForm(forms.Form):
    name = forms.CharField(max_length=32, label='Scenario Name', widget=forms.TextInput(attrs={'autocomplete': 'off'}))


class ScenarioEditForm(forms.Form):
    name = forms.CharField(max_length=32, label='Scenario Name', widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    tasks = forms.IntegerField(min_value=0, label="Number of Tasks", widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    budget = forms.DecimalField(min_value=0, label="Budget €", decimal_places=2, widget=forms.TextInput(attrs={'autocomplete': 'off'}))