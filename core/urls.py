from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    
    # Donor pages (require login)
    path('dashboard/', views.donor_dashboard, name='donor_dashboard'),
    path('profile/', views.donor_profile, name='donor_profile'),
    path('blood-requests/', views.blood_requests, name='blood_requests'),
    path('request-blood/', views.request_blood, name='request_blood'),
    path('accept-request/<str:request_id>/', views.accept_request, name='accept_request'),
    
    # Admin pages
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
]