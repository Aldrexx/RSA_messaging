from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from .views import register, inbox, send_message, delete_message
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    # redirect the root URL to another view, e.g., create_message
    path('', lambda request: redirect('create_message'), name='root'),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('inbox/', inbox, name='inbox'),
    path('send/', send_message, name='send_message'),
    path('message/delete/<int:message_id>/', delete_message, name='delete_message'),
    path('', include('messaging.urls')),
]

from django.urls import path
from . import views

urlpatterns += [
    path('create/', views.create_message, name='create_message'),
    
]

from django.urls import path
from .views import register, inbox, send_message
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns += [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('inbox/', inbox, name='inbox'),
    path('send/', send_message, name='send_message'),
    path('', inbox, name='home'),  # Default 
]
