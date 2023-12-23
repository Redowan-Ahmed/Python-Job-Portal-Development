from django.shortcuts import render
from .models import SupportContact
from django.contrib import messages
from .forms import SupportContactForm


def index(request):
    return render(request, 'index.html')


def SignUp(request):
    return render(request, 'sign-up.html')


def SignIn(request):
    return render(request, 'sign-in.html')


def Account(request):
    return render(request, 'account.html')


def AboutUs(request):
    return render(request, 'about.html')


def Contact(request):
    if request.method == 'POST':
        form = SupportContactForm(request.POST)
        context = {
            'errors': form.errors,
            'form': form
        }
        if form.is_valid():
            name = form.cleaned_data.get('full_name')
            email = form.cleaned_data.get('email')
            number = form.cleaned_data.get('phone_number')
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')
            SupportContact.objects.create(
                full_name=name, email=email, phone_number=number, subject=subject, message=message)
            messages.success(
                request, "Thank your for your Submission, We'll rechout with you soon")
            return render(request, 'contact.html', context=context)
        return render(request, 'contact.html', context=context)

    return render(request, 'contact.html')
