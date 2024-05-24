from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.models import UserProfile
from .models import Testimonials
from .form import TestimonialsForm


def about(request):

    testimonials = Testimonials.objects.filter(
        is_active=True
    )

    testimonial_per_user = []

    for testimonial in testimonials:
        try:
            profile = UserProfile.objects.get(user=testimonial.user)
            testimonial_per_user.append({
                'testimonial': testimonial,
                'profile':  profile
            })
        except UserProfile.DoesNotExist:
            testimonial_per_user.append({
                'testimonial': testimonial,
                'profile': profile
            })

    context = {
        'testimonials': testimonial_per_user,
    }

    return render(request, 'about/about.html', context)


@login_required(login_url='signin')
def testimonial(request):

    url = request.META.get("HTTP_REFERER")

    if request.method == 'POST':
        try:
            comment = Testimonials.objects.get(
                user__id=request.user.id,
                is_active=True
            )

            form = TestimonialsForm(request.POST, instance=comment)
            form.save()

            messages.success(request, "Your comment has been updated!")

            return redirect(url)

        except Testimonials.DoesNotExist:
            form = TestimonialsForm(request.POST)
            if form.is_valid():

                data = Testimonials()
                data.user_id = request.user.id
                data.title = form.cleaned_data['title']
                data.content = form.cleaned_data['content']
                data.ip = request.META.get('REMOTE_ADDR')

                data.save()

                messages.success(request, "Your comment has been submited!")

                return redirect(url)
