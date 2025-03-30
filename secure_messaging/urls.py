from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from messaging.views import register, inbox, send_message, delete_message, admin_panel, toggle_user

urlpatterns = [
    path('', inbox, name='home'),  # Default route goes to inbox
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('inbox/', inbox, name='inbox'),
    path('send/', send_message, name='send_message'),
    path('message/delete/<int:message_id>/', delete_message, name='delete_message'),
    path('admin/', admin_panel, name='admin_panel'),
    path('admin/toggle-user/<int:user_id>/', toggle_user, name='toggle_user'),
]
