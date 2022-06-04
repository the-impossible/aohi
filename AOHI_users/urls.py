from django.urls import path

#My app imports
from AOHI_users.views import (
    IndexView,
    AboutView,
    ContactView,
    DonateView
)

app_name = 'users'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about', AboutView.as_view(), name='about'),
    path('contact', ContactView.as_view(), name='contact'),
    path('donate', DonateView.as_view(), name='donate'),
]