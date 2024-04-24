'''
URL Patterns
'''
from rest_framework.urlpatterns import format_suffix_patterns

from django.views.generic.base import RedirectView
from django.urls import path, include
from django.urls import re_path

from main import views

urlpatterns = [

    path('', views.ExperimentsView.as_view()),

    re_path(r'^admin/login/$', views.LoginView.as_view()),
    
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),

    #txt
    path('robots.txt', views.RobotsTxt, name='robotsTxt'),
    path('ads.txt', views.AdsTxt, name='adsTxt'),
    path('.well-known/security.txt', views.SecurityTxt, name='securityTxt'),
    path('humans.txt', views.HumansTxt, name='humansTxt'),

    #icons
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico'), name='favicon'),
    path('apple-touch-icon-precomposed.png', RedirectView.as_view(url='/static/apple-touch-icon-precomposed.png'), name='favicon'),
    path('apple-touch-icon.png', RedirectView.as_view(url='/static/apple-touch-icon-precomposed.png'), name='favicon'),
    path('apple-touch-icon-120x120-precomposed.png', RedirectView.as_view(url='/static/apple-touch-icon-precomposed.png'), name='favicon'),

    #ui
    path('account/', views.AccountView.as_view(), name='account'),
    path('create-account/', views.CreateAccountView.as_view(), name='create-account'),
    path('verify-account/<str:token>/', views.VerifyAccount.as_view(), name='verify-account'),
    path('verify-account-resend/', views.VerifyAccountResend.as_view(), name='verify-account-resend'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password-reset'),
    path('password-reset-change/<uuid:token>', views.PasswordResetChangeView.as_view(), name='password-reset-change'),
    path('experiments/', views.ExperimentsView.as_view(), name='experiments'),

    #api
    path('get-auth/', views.GetAuthView.as_view()),
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)