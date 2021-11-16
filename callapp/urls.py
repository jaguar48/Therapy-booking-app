from callapp.tokens import Accountactivate
from callapp.views import Homepage
from django.urls import path
from .views import  register, user_login, Accountactivate, edit,contact, call_logs,call_delete,see_feedback
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from . import views

app_name = 'callapp'

urlpatterns =[
    path('', Homepage.as_view(), name="home"),
    path('register/', register, name="register"),
    path('login/', user_login, name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('activate/<uidb64>/<token>/', Accountactivate.as_view(), name='activate'),
    path('edit/', edit, name="edit"),
    path('schedule/',contact, name="schedule"),
    path('password_change/',auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('callapp:password_change_done')),name='password_change'),
    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),
    path('calls', call_logs, name='home'),
    path('<pk>/delete/',call_delete.as_view(), name = "delete"),
    path('<pk>/feedback/',see_feedback.as_view(), name = "feed")

]