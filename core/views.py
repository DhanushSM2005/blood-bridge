from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import BloodRequest
import random
import string

User = get_user_model()


def home(request):
    """Home page view"""
    return render(request, 'home.html')


def user_login(request):
    """Login view"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Authenticate using email as username
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('donor_dashboard')  # FIXED: Changed from 'dashboard' to 'donor_dashboard'
        else:
            messages.error(request, 'Invalid email or password')
    
    return render(request, 'login.html')


def user_register(request):
    """Registration view"""
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        blood_group = request.POST.get('blood_group')
        city = request.POST.get('city')
        password = request.POST.get('password')
        
        # Check if user already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, 'This email is already registered')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered')
        else:
            # Create new user
            try:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    full_name=full_name,
                    blood_group=blood_group,
                    city=city
                )
                messages.success(request, 'Registration successful! Please login.')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
    
    return render(request, 'register.html')


@login_required
def donor_dashboard(request):
    """Donor dashboard view"""
    # Get pending blood requests
    blood_requests = BloodRequest.objects.filter(status='Pending')[:10]
    
    context = {
        'blood_requests': blood_requests,
        'user': request.user
    }
    return render(request, 'donor_dashboard.html', context)


@login_required
def donor_profile(request):
    """Donor profile view"""
    if request.method == 'POST':
        # Update profile
        request.user.full_name = request.POST.get('full_name', request.user.full_name)
        request.user.phone = request.POST.get('phone', request.user.phone)
        request.user.city = request.POST.get('city', request.user.city)
        request.user.blood_group = request.POST.get('blood_group', request.user.blood_group)
        request.user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('donor_profile')
    
    return render(request, 'donor_profile.html', {'user': request.user})


@login_required
def blood_requests(request):
    """View all blood requests"""
    all_requests = BloodRequest.objects.all().order_by('-created_at')
    
    context = {
        'blood_requests': all_requests,
        'user': request.user
    }
    return render(request, 'blood_requests.html', context)


@login_required
def request_blood(request):
    """Create blood request view"""
    if request.method == 'POST':
        blood_group = request.POST.get('blood_group')
        units_required = request.POST.get('units_required')
        hospital_name = request.POST.get('hospital_name')
        location = request.POST.get('location')
        emergency_level = request.POST.get('emergency_level')
        
        # Generate unique request ID
        request_id = 'REQ' + ''.join(random.choices(string.digits, k=6))
        
        # Create blood request
        BloodRequest.objects.create(
            request_id=request_id,
            blood_group=blood_group,
            units_required=units_required,
            hospital_name=hospital_name,
            location=location,
            emergency_level=emergency_level,
            requested_by=request.user
        )
        
        messages.success(request, f'Blood request {request_id} submitted successfully!')
        return redirect('donor_dashboard')
    
    return render(request, 'request_blood.html')


@login_required
def accept_request(request, request_id):
    """Accept a blood request"""
    try:
        blood_request = BloodRequest.objects.get(request_id=request_id)
        blood_request.assigned_to = request.user
        blood_request.status = 'In Progress'
        blood_request.save()
        messages.success(request, f'You have accepted request {request_id}')
    except BloodRequest.DoesNotExist:
        messages.error(request, 'Request not found')
    
    return redirect('donor_dashboard')


@login_required
def admin_dashboard(request):
    """Admin dashboard view"""
    # Check if user is staff/admin
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('donor_dashboard')
    
    all_requests = BloodRequest.objects.all().order_by('-created_at')
    
    # Statistics
    total_requests = all_requests.count()
    pending_requests = all_requests.filter(status='Pending').count()
    completed_requests = all_requests.filter(status='Completed').count()
    in_progress_requests = all_requests.filter(status='In Progress').count()
    
    context = {
        'blood_requests': all_requests,
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'completed_requests': completed_requests,
        'in_progress_requests': in_progress_requests,
    }
    return render(request, 'admin_dashboard.html', context)


def user_logout(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')