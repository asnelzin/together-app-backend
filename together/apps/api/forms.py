from django import forms


class NamePasswordForm(forms.Form):
    name = forms.CharField(max_length=200)
    password = forms.CharField(max_length=50)


class NamePassCoordForm(forms.Form):
    name = forms.CharField(max_length=200)
    latitude = forms.FloatField(min_value=-90, max_value=90)
    longitude = forms.FloatField(min_value=-180, max_value=180)