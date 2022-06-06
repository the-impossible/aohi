from django.urls import path

#My app imports
from AOHI_auth.views import (
    RegisterView,
    LoginView,
    LogoutView,
    ListOrphansView,
    OrphanProfileView,
    RequestAdoptionView,
    ListOrphansAdminView,
    RequestAdoptionListView,
    RequestAdoptionListAdminView,
    MakePaymentView,
    MyDonationListView,
    MyAdoptionListView,
    AdoptionSuccessfulView,
)

app_name = 'auth'

urlpatterns = [
    # AUTH
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

    # ORPHAN
    path('list_orphans', ListOrphansView.as_view(), name='list_orphans'),
    path('list_orphans_admin', ListOrphansAdminView.as_view(), name='list_orphans_admin'),
    path('orphan_profile/<int:orphan_id>', OrphanProfileView.as_view(), name='orphan_profile'),
    path('request_orphan', RequestAdoptionView.as_view(), name='request_orphan'),
    path('request_list', RequestAdoptionListView.as_view(), name='request_list'),
    path('request_list_admin', RequestAdoptionListAdminView.as_view(), name='request_list_admin'),

    # PAYMENT
    path('make_payment/<int:user_id>/<int:orphan_id>', MakePaymentView.as_view(), name='make_payment'),

    # DONATIONS
    path('my_donations', MyDonationListView.as_view(), name='my_donations'),

    # ADOPTIONS
    path('my_adoptions', MyAdoptionListView.as_view(), name='my_adoptions'),
    path('success/<int:user_id>/<int:orphan_id>', AdoptionSuccessfulView.as_view(), name='success'),

]