# My django imports
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.contrib import messages

# My app imports
from AOHI_admin.forms import DonationForm
from AOHI_auth.views import stripe_payment
from AOHI_users.models import Donations

import stripe
stripe.api_key = "sk_test_51L5Xs6GCAqCizi1RncjTC84yc0J7jaecLFB5gj07ZDNWCREFyEylsunXTltlQleL3lWzEcLsqIFCInvn6wGYu2Xa00cIHRZjMz"

# Create your views here.
class IndexView(View):
    def get(self, request):
        return render(request, 'aohi/index.html')

class AboutView(View):
    def get(self, request):
        return render(request, 'aohi/about.html')

class ContactView(View):
    def get(self, request):
        return render(request, 'aohi/contact.html')

class DonateView(View):
    def get(self, request):
        form = DonationForm()
        return render(request, 'aohi/donate.html', context={'form':form})

    def post(self, request):
        form = DonationForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            email = form.email
            firstname = form.firstname
            lastname = form.lastname
            phone = form.phone
            amount = int(form.amount)
            source = request.POST.get('stripeToken')

            stripe_payment(email, firstname, lastname, amount, source)

            Donations.objects.create(
                firstname=firstname,
                lastname=lastname,
                phone=phone,
                amount=amount,
                email=email
            )

            messages.success(request, 'Thank you for your generous donation')
            return redirect('users:donate')

        messages.error(request, 'Error processing donation')
        return render(request, 'aohi/donate.html', context={'form':form})
