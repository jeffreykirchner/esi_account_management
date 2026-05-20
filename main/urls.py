'''
URL Patterns
'''
from rest_framework.urlpatterns import format_suffix_patterns
from oauth2_provider import urls as oauth2_urls
import oauth2_provider.views as oauth2_views

from django.views.generic.base import RedirectView
from django.urls import path, include
from django.urls import re_path


from main import views

# OAuth2 provider endpoints
oauth2_endpoint_views = [   
    path('authorize/', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    path('token/', oauth2_views.TokenView.as_view(), name="token"),
    path('revoke-token/', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

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
    path('experiments-manage/<int:pk>/', views.ExperimentsManageView.as_view(), name='experiments-manage'),

    #api
    path('get-auth/', views.GetAuthView.as_view()),

    #oauth
    path("o/", include((oauth2_endpoint_views, 'oauth2_provider'), namespace='oauth2_provider')),
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)