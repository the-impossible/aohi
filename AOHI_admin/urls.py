from django.urls import path

#My app imports
from AOHI_admin.views import (
    DashboardView,
    CreateStaffView,
    ListStaffView,
    CreateUsersView,
    ListUsersView,
    ListAdminView,
    CreateOrphanView,
    ListOrphansView,
    ProfileView,
    ListDonationsView,
    MakeDonationView,
    AdoptionListView,
)

app_name = 'aohi_admin'

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name='dashboard'),

    # STAFF
    path('create_staff/<str:type>', CreateStaffView.as_view(), name='create_staff'),
    path('list_staff', ListStaffView.as_view(), name='list_staff'),
    path('list_admin', ListAdminView.as_view(), name='list_admin'),

    #USER
    path('create_user', CreateUsersView.as_view(), name='create_user'),
    path('list_users', ListUsersView.as_view(), name='list_users'),

    #ORPHAN
    path('create_orphan', CreateOrphanView.as_view(), name='create_orphan'),
    path('list_orphans', ListOrphansView.as_view(), name='list_orphans'),

    #PROFILE
    path('profile_view/<int:user_id>', ProfileView.as_view(), name='profile_view'),

    #DONATIONS
    path('donations', ListDonationsView.as_view(), name='donations'),
    path('make_donation/<int:user_id>', MakeDonationView.as_view(), name='make_donation'),

    #ADOPTIONS
    path('adoptions', AdoptionListView.as_view(), name='adoptions'),

]