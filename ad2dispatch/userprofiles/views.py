from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from pages.models import get_top_pages
from .models import Volunteer
from .forms import ProfileForm


@login_required
def profile(request):
    try:
        volunteer = Volunteer.objects.get(user=request.user)
    except Volunteer.DoesNotExist:
        volunteer = Volunteer(user=request.user)
        volunteer.save()
    context = {'volunteer': volunteer}
    if request.method == 'POST':
        userform = ProfileForm(request.POST)
        if userform.is_valid():
            if userform.save(request.user, volunteer):
                context['flash_type'] = 'success'
                context['flash_message'] = 'Saved!'
            else:
                context['flash_type'] = 'danger'
                context['flash_message'] = 'An error occurred.'
    else:
        userform = ProfileForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'username': request.user.username,
            'email': request.user.email,
            'service': volunteer.service,
            'unit': volunteer.unit,
            'rank': volunteer.rank,
            'phone_number': volunteer.phone_number,
            'vehicle_desc': volunteer.vehicle_desc,
            'sup_name': volunteer.sup_name,
            'sup_phone': volunteer.sup_phone,
            'accepted_waiver': volunteer.accepted_waiver,
            'reviewed_profile': volunteer.reviewed_profile
        })
        if not volunteer.reviewed_profile:
            context['flash_type'] = 'warning'
            context['flash_message'] = 'Your profile must be updated. Please click "Save" to verify.'

    top_pages = get_top_pages()

    context['form'] = userform
    context['top_pages'] = top_pages

    return render(request, 'profile.html', context)
