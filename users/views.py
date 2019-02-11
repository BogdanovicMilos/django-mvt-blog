from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import BadHeaderError, send_mail
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ContactForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            sender_email = form.cleaned_data.get('email')
            recevier_email = settings.EMAIL_HOST_USER
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')
            try:
                send_mail(subject, message, sender_email, [recevier_email], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return render(request, 'users/contact_complete.html')
    return render(request, 'users/contact.html')
