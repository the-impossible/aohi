from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect


# My App imports
from AOHI_auth.models import Accounts
from AOHI_admin.models import Orphans, Adoptions, Payments
from AOHI_auth.views import stripe_payment
from AOHI_users.models import AdoptionInfo, Donations
from AOHI_auth.forms import AccountCreationForm
from AOHI_admin.forms import AdoptionInfoForm, UserAccountForm, OrphansForm, UpdateAccountForm, AccountPictureForm,DonationForm


# Create your views here.
class DashboardView(View, LoginRequiredMixin):
    def get(self, request):
        donors = Accounts.objects.filter(is_staff=False).count()
        staffs = Accounts.objects.filter(is_staff=True).count()
        admins = Accounts.objects.filter(is_superuser=True).count()
        all_donations = Donations.objects.all().count()
        orphans = Orphans.objects.all().count()
        adoptions = Adoptions.objects.all().count()
        # ALL_DONATIONS
        donations_made = Donations.objects.all()
        amount = 0
        for donations in donations_made:
            amount += donations.amount

        # MY_DONATION
        my_donation = Donations.objects.filter(email=request.user)
        no_my_donation = Donations.objects.filter(email=request.user).count()
        my_amount = 0
        for donations in my_donation:
            my_amount += donations.amount

        # MY_ADOPTION
        my_no_adoption = Adoptions.objects.filter(user=request.user).count()

        # ADOPTION_AMOUNT
        all_adoptions = Payments.objects.all()
        adoption_amount = 0
        for donations in all_adoptions:
            adoption_amount += donations.amount

        context = {
            'donors':donors,
            'staffs':staffs,
            'admins':admins,
            'all_donations':all_donations,
            'orphans':orphans,
            'adoptions':adoptions,
            'amount':amount,
            'my_amount':my_amount,
            'no_my_donation':no_my_donation,
            'my_no_adoption':my_no_adoption,
            'adoption_amount':adoption_amount
        }
        return render(request,'admin/dashboard.html', context)

class CreateStaffView(View, LoginRequiredMixin):
    form = UserAccountForm()
    def get(self, request, type):
        context = {'form':self.form}

        if type == 'a':
            context['type'] = 'Admin'
        else:
            context['type'] = 'Staff'
        return render(request,'admin/create_staff.html', context)

    def post(self, request, type):
        form = UserAccountForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)

            user.is_staff = True
            user.set_password(user.password)

            if type == 'a':
                user.is_superuser = True

            user.save()
            messages.success(request, ('Creation Successful and user active'))
            context = {'form':self.form}
            return render(request, 'admin/create_staff.html', context)

        messages.error(request, ('Invalid Submitted form!!'))
        context={'form':form}
        return render(request, 'admin/create_staff.html', context)

class ListStaffView(ListView, LoginRequiredMixin):
    template_name = 'admin/list_staff.html'
    queryset = Accounts.objects.filter(is_staff=True)
    context_object_name = 'staffs'

class CreateUsersView(View, LoginRequiredMixin):
    info = AdoptionInfoForm()
    form = UserAccountForm()

    def get(self, request):
        context = {'form':self.form, 'info':self.info}
        return render(request,'admin/create_user.html', context)

    def post(self, request):
        form = UserAccountForm(request.POST, request.FILES)
        info = AdoptionInfoForm(request.POST)

        if form.is_valid() and info.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)

            info_form = info.save(commit=False)
            info_form.acct = user

            user.save()
            info_form.save()
            messages.success(request, ('Creation Successful and user active'))
            context = {'form':self.form, 'info':self.info}
            return render(request, 'admin/create_user.html', context)

        messages.error(request, ('Invalid Submitted form!!'))
        context={'form':form, 'info':info}
        return render(request, 'admin/create_user.html', context)

class ListUsersView(ListView, LoginRequiredMixin):
    template_name = 'admin/list_users.html'
    queryset = Accounts.objects.filter(is_staff=False)
    context_object_name = 'users'

class ListAdminView(ListView, LoginRequiredMixin):
    template_name = 'admin/list_admin.html'
    queryset = Accounts.objects.filter(is_superuser=True)
    context_object_name = 'admins'

class CreateOrphanView(View, LoginRequiredMixin):
    form = OrphansForm()

    def get(self, request):
        context = {'form':self.form}
        return render(request,'admin/create_orphan.html', context)

    def post(self, request):
        form = OrphansForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, ('Record Saved Successfully!!'))
            context = {'form':self.form }
            return render(request, 'admin/create_orphan.html', context)

        messages.error(request, ('Invalid Submitted form!!'))
        context={'form':form}
        return render(request, 'admin/create_orphan.html', context)

class ListOrphansView(ListView, LoginRequiredMixin):
    template_name = 'admin/list_orphans.html'
    queryset = Orphans.objects.all()
    context_object_name = 'orphans'

class ProfileView(View, LoginRequiredMixin):
    def get(self, request, user_id):
        try:
            acct = Accounts.objects.get(id=user_id)
            form = UpdateAccountForm(instance=acct)
            pic_form = AccountPictureForm(instance=acct)
            if acct.is_staff:
                context = {
                    'user':acct,
                    'pic_form':pic_form,
                    'form':form,
                }
            else:
                try:
                    aohi_user = AdoptionInfo.objects.get(acct_id=user_id)
                    form2 = AdoptionInfoForm(instance=aohi_user)
                    context = {
                        'user':acct,
                        'pic_form':pic_form,
                        'form':form,
                        'form2':form2,

                        'aohi_user':aohi_user,
                    }
                except ObjectDoesNotExist:
                    context = {
                        'user':acct,
                        'pic_form':pic_form,
                        'form':form,
                        'form2':AdoptionInfoForm(),
                    }
        except ObjectDoesNotExist:
            messages.error(request, ('User profile not found!!'))
            return redirect('aohi_admin:dashboard')
        return render(request,'admin/profile.html', context)

    def post(self, request, user_id):
        if 'picture' in request.POST:
            acct = Accounts.objects.get(id=user_id)
            pic_form = AccountPictureForm(request.POST, request.FILES, instance=acct)
            if pic_form.is_valid():
                pic_form.save()
                messages.success(request, ('Profile Picture Updated successfully!!'))
            else:
                messages.error(request, ('Error Uploading Profile!'))
            return redirect('aohi_admin:profile_view', user_id)

        if 'info' in request.POST:
            acct = Accounts.objects.get(id=user_id)
            form = UpdateAccountForm(data=request.POST, instance=acct)

            context = {'form':form, 'user':acct}

            if not acct.is_staff:
                try:
                    aohi_user = AdoptionInfo.objects.get(acct_id=user_id)
                    form2 = AdoptionInfoForm(data=request.POST, instance=aohi_user)
                except:
                    form2 = AdoptionInfoForm(request.POST)
                    if form.is_valid() and form2.is_valid():
                        info_form = form2.save(commit=False)
                        info_form.acct = acct
                        form.save()
                        form2.save()
                        messages.success(request, ('Profile Info Updated successfully'))
                        return redirect('aohi_admin:profile_view', user_id)

                    context['form2'] = form2
                    messages.error(request, ('Error Updating Profile!!'))
                    return render(request,'admin/profile.html', context)


                context['form2'] = form2
                context['aohi_user'] = aohi_user

                if form.is_valid() and form2.is_valid():
                    form.save()
                    form2.save()
                    messages.success(request, ('Profile Info Updated successfully'))
                    return redirect('aohi_admin:profile_view', user_id)

            if acct.is_staff:
                if form.is_valid():
                    form.save()
                    messages.success(request, ('Profile Info Updated successfully'))
                    return redirect('aohi_admin:profile_view', user_id)
                context = {'form':form, 'user':acct}

            messages.error(request, ('Error Updating Profile!!'))
            return render(request,'admin/profile.html', context)

        if 'change_pass' in request.POST:
            try:
                user = Accounts.objects.get(pk=user_id)
            except Accounts.DoesNotExist:
                messages.error(request, 'Oops user does not exist!')
                return redirect('aohi_admin:profile_view', user_id)
            else:
                password = request.POST['password']
                password1 = request.POST['password1']

                if(password1 != password):
                    messages.error(request, 'Password don\'t match!')
                    return redirect('aohi_admin:profile_view', user_id)

                if(len(password1) < 6):
                    messages.error(request, 'Password too short!')
                    return redirect('aohi_admin:profile_view', user_id)

                user.set_password(password)
                messages.success(request, 'Password has been changed user can now login with the new password')
                user.save()

            if request.user.is_superuser:
                return redirect('aohi_admin:profile_view', user_id)
            return redirect('auth:login')

        if 'delete' in request.POST:
            try:
                acct = Accounts.objects.get(id=user_id)
                acct.delete()
                messages.success(request, (f'{acct} has been deleted successfully!!'))
            except:
                messages.error(request, (f'Failed in deleting {acct}'))
            return redirect('aohi_admin:list_users')

class ListDonationsView(ListView, LoginRequiredMixin):
    template_name = 'admin/list_donation.html'
    queryset = Donations.objects.all().order_by('-id')
    context_object_name = 'donations'

class MakeDonationView(View, LoginRequiredMixin):
    def get(self, request, user_id):
        try:
            admin_or_user = request.user
            if not admin_or_user.is_superuser:
                user = Accounts.objects.get(id=user_id)
                form = DonationForm(instance=user)
            else:
                form = DonationForm()
            return render(request,'admin/create_donation.html', context={'form':form})
        except ObjectDoesNotExist:
            messages.error(request, 'User profile not found')
            return redirect('aohi_admin:dashboard')

    def post(self, request, user_id):
        try:
            admin_or_user = request.user
            user = Accounts.objects.get(id=user_id)
            form = DonationForm(request.POST)

            if form.is_valid():
                form = form.save(commit=False)
                source = request.POST.get('stripeToken')
                if not admin_or_user.is_superuser:
                    amount = int(form.amount)
                    email = user.email
                    firstname = user.firstname
                    lastname = user.lastname
                    phone = user.phone
                    stripe_payment(email, firstname, lastname, amount, source)
                    Donations.objects.create(
                        firstname=firstname,
                        lastname=lastname,
                        phone=phone,
                        amount=amount,
                        email=email
                    )
                else:
                    amount = int(form.amount)
                    email = form.email
                    firstname = form.firstname
                    lastname = form.lastname
                    phone = form.phone
                    stripe_payment(email, firstname, lastname, amount, source)

                    Donations.objects.create(
                        firstname=firstname,
                       lastname=lastname,
                       phone=phone,
                       amount=amount,
                       email=email
                    )
                messages.success(request, 'Thank you for your generous donation')

            return redirect('aohi_admin:make_donation', user_id)

        except ObjectDoesNotExist:
            messages.error(request, 'User profile not found')
            return redirect('aohi_admin:dashboard')

        return redirect('aohi_admin:make_donation', user_id)

class AdoptionListView(View, LoginRequiredMixin):
    def get(self, request):
        adoptions = Adoptions.objects.all()
        return render(request, 'admin/list_adoption.html', context={'adoptions':adoptions})

