# My django imports
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.contrib import messages
from django.views.generic import ListView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin


# My app imports
from AOHI_auth.models import Accounts
from AOHI_admin.models import Orphans, RequestAdoption, Payments, Adoptions
from AOHI_auth.forms import AccountCreationForm
from AOHI_users.models import Donations
from AOHI_admin.forms import OrphanPictureForm, UpdateOrphansForm, PaymentForm

import stripe
stripe.api_key = "sk_test_51L5Xs6GCAqCizi1RncjTC84yc0J7jaecLFB5gj07ZDNWCREFyEylsunXTltlQleL3lWzEcLsqIFCInvn6wGYu2Xa00cIHRZjMz"

# Create your views here.
class RegisterView(View, LoginRequiredMixin):
    def get(self, request):
        form = AccountCreationForm()
        context = {'form':form}
        return render(request,'auth/register.html', context)

    def post(self, request):
        form = AccountCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, ('Creation Successful you can now login'))
            return redirect('auth:login')
        return render(request,'auth/register.html', {'form':form})

class LoginView(View, LoginRequiredMixin):
    def get(self, request):

        return render(request,'auth/login.html')

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']

        if email and password:
            # Authenticate user
            user = authenticate(request, email=email.lower(), password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'You are now signed in {user.get_firstname()} {user.get_lastname()}')
                    return redirect('aohi_admin:dashboard')
                else:
                    messages.warning(request, 'Account not active contact the administrator')
                    return redirect('auth:login')
            else:
                messages.warning(request, 'Invalid login credentials')
                return redirect('auth:login')
        else:
            messages.error(request, 'All fields are required!!')
            return redirect('auth:login')

class LogoutView(View, LoginRequiredMixin):
    def post(self, request):
        logout(request)
        messages.success(request, 'You are now signed out!')
        return redirect('auth:login')

class ListOrphansView(ListView):
    template_name = 'auth_users/list_orphans.html'
    queryset = Orphans.objects.filter(status=True)
    context_object_name = 'orphans'
    extra_context = {'type':'View'}

class ListOrphansAdminView(ListView):
    template_name = 'auth_users/list_orphans.html'
    queryset = Orphans.objects.all()
    context_object_name = 'orphans'
    extra_context = {'type':'Manage'}

class OrphanProfileView(View, LoginRequiredMixin):
    def get(self, request, orphan_id):
        try:
            orphan = Orphans.objects.get(id=orphan_id)
            pic_form = OrphanPictureForm(instance=orphan)
            form = UpdateOrphansForm(instance=orphan)

            context = {'orphan':orphan, 'pic_form':pic_form, 'form':form}
        except ObjectDoesNotExist:
            messages.error(request, ('Orphan profile not found!!'))

        return render(request,'auth_users/orphan_profile.html', context)

    def post(self, request, orphan_id):

        if 'info' in request.POST:
            orphan = Orphans.objects.get(id=orphan_id)
            form = UpdateOrphansForm(request.POST, instance=orphan)
            pic_form = OrphanPictureForm(instance=orphan)

            if form.is_valid():
                form.save()

                messages.success(request, ('Profile Updated Successfully!!'))
                return redirect('auth:orphan_profile', orphan_id)

            messages.error(request, ('Error Updating Profile'))
            context = {'form':form, 'orphan':orphan, 'pic_form':pic_form,}

        if 'picture' in request.POST:
            orphan = Orphans.objects.get(id=orphan_id)
            form = UpdateOrphansForm(request.POST, instance=orphan)
            pic_form = OrphanPictureForm(request.POST, request.FILES, instance=orphan)

            if pic_form.is_valid():
                pic_form.save()
                messages.success(request, ('Profile Picture Updated successfully!!'))
                return redirect('auth:orphan_profile', orphan_id)

            context = {'form':form, 'orphan':orphan, 'pic_form':pic_form,}
            messages.error(request, ('Error Uploading Profile!'))

        if 'delete' in request.POST:
            try:
                acct = Orphans.objects.get(id=orphan_id)
                acct.delete()
                messages.success(request, (f'{acct} has been deleted successfully!!'))
            except:
                messages.error(request, (f'Failed in deleting account'))
            return redirect('auth:list_orphans')

        return render(request,'auth_users/orphan_profile.html', context)

class RequestAdoptionView(View, LoginRequiredMixin):

    def post(self, request):
        user_id = int(request.POST['user_id'])
        orphan_id = int(request.POST['orphan_id'])

        try:
            user = Accounts.objects.get(id=user_id)
            orphan = Orphans.objects.get(id=orphan_id)
            try:
                RequestAdoption.objects.get(user=user, orphan=orphan)
                messages.warning(request, f"Request: has been Filed before")
            except:
                RequestAdoption.objects.create(user=user, orphan=orphan)
                messages.success(request, 'Request has been Filed Check request page to view progress')
        except:
            messages.error(request, 'Something went wrong, unable to file request')

        return redirect('auth:request_list')

class RequestAdoptionListView(ListView):
    def get(self, request):
        adoptions = RequestAdoption.objects.filter(user=request.user)
        context = {'adoptions':adoptions}
        return render(request, 'auth_users/adoption_request_list.html', context)

class RequestAdoptionListAdminView(ListView):
    def get(self, request):
        adoptions = RequestAdoption.objects.filter(adopted=False)
        context = {'adoptions':adoptions}
        return render(request, 'admin/adoption_request_list_admin.html', context)

    def post(self, request):
        user_id = int(request.POST['user_id'])
        orphan_id = int(request.POST['orphan_id'])

        try:
            user = Accounts.objects.get(id=user_id)
            orphan = Orphans.objects.get(id=orphan_id)

            to_approve = RequestAdoption.objects.get(orphan=orphan, user=user)
            if 'approve' in request.POST:
                to_approve.status = True
                to_approve.save()
                messages.success(request, f'{user} Request has been approved for {orphan.firstname}')

            if 'cancel' in request.POST:
                to_approve.status = False
                to_approve.save()
                messages.success(request, f'{user} Request has been Cancelled for {orphan.firstname}')

            return redirect('auth:request_list_admin')
        except:
            messages.error(request, f'Unable to approve adoption request')
            return redirect('auth:request_list_admin')

def stripe_payment(email, firstname, lastname, amount, source):
    try:
        customer = stripe.Customer.create(
            email = email,
            name = f'{firstname} {lastname}',
            description = 'AOHI Child Adoption',
            source = source
        )

        charge = stripe.Charge.create(
            customer=customer,
            amount=amount * 100,
            currency='NGN',
            description='AOHI Child Adoption',
        )
    except stripe.error.CardError:
        messages.error(request, ('Your card has insufficient funds!!'))

class MakePaymentView(ListView, LoginRequiredMixin):
    def get(self, request, user_id, orphan_id):
        try:
            user = Accounts.objects.get(id=user_id)
            orphan = Orphans.objects.get(id=orphan_id)
            form = PaymentForm(instance=user)
            context = {
                'form':form,
                'orphan':orphan,
            }
        except ObjectDoesNotExist:
            messages.error(request, ('User profile not found!!'))
            return redirect('aohi_admin:dashboard')

        return render(request, 'auth_users/make_payment.html', context)

    def post(self, request, user_id, orphan_id):

        try:
            user = Accounts.objects.get(id=user_id)

            email = user.email
            firstname = user.firstname
            lastname = user.lastname
            phone = user.phone
            amount = 200000
            source = request.POST.get('stripeToken')

            stripe_payment(email, firstname, lastname, amount, source)

        except ObjectDoesNotExist:
            messages.error(request, ('User profile not found!!'))
            return redirect('auth:make_payment', user_id, orphan_id)

        else:
            orphan = Orphans.objects.get(id=orphan_id)
            orphan.status = False

            to_adopt = RequestAdoption.objects.get(orphan=orphan, user=user)
            # adopted and status become true for the user who made payment
            to_adopt.adopted = True
            to_adopt.save()
            orphan.save()

            # adopted(true) status(false) for other
            not_me_but_adopted = RequestAdoption.objects.filter(orphan=orphan)
            for user in not_me_but_adopted:
                user.adopted = True
                user.save()

            user = Accounts.objects.get(id=user_id)
            # Update Payment Table
            Payments.objects.create(orphan=orphan, amount=amount, user=user)

            #Update Adoption Table
            Adoptions.objects.create(user=user, orphan=orphan, status=True)

            messages.success(request, 'Payment successful')

            return redirect('auth:request_list')

        return redirect('auth:make_payment', user_id, orphan_id)

class AdoptionListView(ListView, LoginRequiredMixin):
    def get(self, request, user_id):
        try:
            user = Accounts.objects.get(id=user_id)
            adoptions = Adoptions.objects.filter(user=user)
            context = {
                'adoptions':adoptions,
            }
        except ObjectDoesNotExist:
            messages.error(request, ('User profile not found!!'))
            return redirect('aohi_admin:dashboard')

        return render(request, 'auth_users/adoptions.html', context)

class MyDonationListView(View, LoginRequiredMixin):
    def get(self, request):
        donations = Donations.objects.filter(email=request.user)
        return render(request, 'admin/list_donation.html', context={'donations':donations})

class MyAdoptionListView(View, LoginRequiredMixin):
    def get(self, request):
        adoptions = Adoptions.objects.filter(user=request.user)
        return render(request, 'admin/list_adoption.html', context={'adoptions':adoptions})