from django import forms


class ProfileForm(forms.Form):
    first_name = forms.CharField(
        required=True,
        label='First Name:',
        max_length=32,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))
    last_name = forms.CharField(
        required=True,
        label='Last Name:',
        max_length=32,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))
    username = forms.CharField(
        required=True,
        label='Username:',
        max_length=32,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'readonly': 'readonly'}))
    email = forms.EmailField(
        required=True,
        label='Email:',
        max_length=64,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'readonly': 'readonly'}))
    service = forms.CharField(
        label='Service:',
        max_length=24,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))
    unit = forms.CharField(
        label='Unit:',
        max_length=64,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))
    rank = forms.CharField(
        label='Rank:',
        max_length=16,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))
    phone_number = forms.CharField(
        required=True,
        label='Phone Number:',
        max_length=14,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))
    vehicle_desc = forms.CharField(
        required=True,
        label='Vehicle Description:',
        max_length=128,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))
    sup_name = forms.CharField(
        label='Supervisor Name:',
        max_length=64,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))
    sup_phone = forms.CharField(
        label='Supervisor Phone:',
        max_length=14,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))
    accepted_waiver = forms.BooleanField(
         required=True,
         label='Accept Waiver:',
         widget=forms.CheckboxInput())

    def save(self, user, volunteer):
        try:
            data = self.cleaned_data

            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.save()

            volunteer.service = data['service']
            volunteer.unit = data['unit']
            volunteer.rank = data['rank']
            volunteer.phone_number = data['phone_number']
            volunteer.vehicle_desc = data['vehicle_desc']
            volunteer.sup_name = data['sup_name']
            volunteer.sup_phone = data['sup_phone']
            volunteer.accepted_waiver = data['accepted_waiver']
            volunteer.reviewed_profile = True
            volunteer.save()

            return True

        except Exception:
            return False
