from django import forms


class EventManageDateSelectForm(forms.Form):
    start_date = forms.CharField(
        label='Start Date:',
        max_length=7,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))
    end_date = forms.CharField(
        label='End Date:',
        max_length=7,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))
