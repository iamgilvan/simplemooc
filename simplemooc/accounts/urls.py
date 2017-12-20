from django.conf.urls import url , include
from django.contrib.auth.views import login
from django.contrib.auth.views import logout
from simplemooc.accounts.views import register
from simplemooc.accounts.views import dashboard

urlpatterns = [
    url(r'^$', dashboard ,name='dashboard'),
    url(r'^entrar/$', login, {'template_name': 'accounts/login.html'} ,name='login'),
    url(r'^cadastre-se/$', register, name='register'),
    url(r'^sair/$', logout, {'next_page': 'core:home'} ,name='logout'),
]
