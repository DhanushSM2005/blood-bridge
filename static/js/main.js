// Blood Bridge - Main JavaScript File

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // Form Validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(form)) {
                e.preventDefault();
            }
        });
    });

    // Availability Toggle
    const availabilityToggle = document.querySelector('.toggle-switch');
    if (availabilityToggle) {
        availabilityToggle.addEventListener('click', function() {
            this.classList.toggle('off');
            const isAvailable = !this.classList.contains('off');
            updateAvailability(isAvailable);
        });
    }

    // Accept Request Buttons
    const acceptButtons = document.querySelectorAll('.btn-accept');
    acceptButtons.forEach(button => {
        button.addEventListener('click', function() {
            const requestId = this.getAttribute('data-request-id');
            acceptBloodRequest(requestId);
        });
    });

    // Initialize tooltips and popovers if using Bootstrap
    initializeTooltips();

    // Add smooth scrolling
    addSmoothScrolling();
});

// Form Validation Function
function validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('input[required], select[required]');
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            showError(input, 'This field is required');
            isValid = false;
        } else {
            clearError(input);
        }

        // Email validation
        if (input.type === 'email' && input.value.trim()) {
            if (!isValidEmail(input.value)) {
                showError(input, 'Please enter a valid email address');
                isValid = false;
            }
        }

        // Password validation
        if (input.type === 'password' && input.value.trim()) {
            if (input.value.length < 6) {
                showError(input, 'Password must be at least 6 characters');
                isValid = false;
            }
        }
    });

    return isValid;
}

// Show error message
function showError(input, message) {
    const formGroup = input.closest('.form-group');
    let errorDiv = formGroup.querySelector('.error-message');
    
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.style.color = '#c9302c';
        errorDiv.style.fontSize = '12px';
        errorDiv.style.marginTop = '5px';
        formGroup.appendChild(errorDiv);
    }
    
    errorDiv.textContent = message;
    input.style.borderColor = '#c9302c';
}

// Clear error message
function clearError(input) {
    const formGroup = input.closest('.form-group');
    const errorDiv = formGroup.querySelector('.error-message');
    
    if (errorDiv) {
        errorDiv.remove();
    }
    
    input.style.borderColor = '#ddd';
}

// Email validation
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Update Availability Status
function updateAvailability(isAvailable) {
    // This would typically make an AJAX call to update the server
    const status = isAvailable ? 'available' : 'unavailable';
    
    // Show notification
    showNotification(
        isAvailable ? 'You are now available for blood donation' : 'You are now unavailable for blood donation',
        'success'
    );
    
    // In a real application, this would be an AJAX call:
    // fetch('/api/update-availability', {
    //     method: 'POST',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify({ available: isAvailable })
    // });
}

// Accept Blood Request
function acceptBloodRequest(requestId) {
    if (confirm('Are you sure you want to accept this blood request?')) {
        // Show loading state
        const button = document.querySelector(`[data-request-id="${requestId}"]`);
        const originalText = button.textContent;
        button.textContent = 'Processing...';
        button.disabled = true;

        // Simulate API call
        setTimeout(() => {
            showNotification('Blood request accepted successfully!', 'success');
            button.textContent = 'Accepted';
            button.style.backgroundColor = '#4caf50';
            
            // In a real application, this would be an AJAX call:
            // fetch(`/api/accept-request/${requestId}`, {
            //     method: 'POST',
            //     headers: { 'Content-Type': 'application/json' }
            // })
            // .then(response => response.json())
            // .then(data => {
            //     showNotification('Blood request accepted!', 'success');
            // });
        }, 1000);
    }
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background-color: ${type === 'success' ? '#4caf50' : type === 'error' ? '#f44336' : '#2196F3'};
        color: white;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Initialize tooltips (if using Bootstrap or similar)
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltipText = this.getAttribute('data-tooltip');
            showTooltip(this, tooltipText);
        });
        
        element.addEventListener('mouseleave', function() {
            hideTooltip();
        });
    });
}

// Show tooltip
function showTooltip(element, text) {
    const tooltip = document.createElement('div');
    tooltip.className = 'custom-tooltip';
    tooltip.style.cssText = `
        position: absolute;
        background-color: #333;
        color: white;
        padding: 5px 10px;
        border-radius: 4px;
        font-size: 12px;
        z-index: 10000;
        pointer-events: none;
    `;
    tooltip.textContent = text;
    document.body.appendChild(tooltip);
    
    const rect = element.getBoundingClientRect();
    tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
    tooltip.style.left = (rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2)) + 'px';
}

// Hide tooltip
function hideTooltip() {
    const tooltip = document.querySelector('.custom-tooltip');
    if (tooltip) {
        tooltip.remove();
    }
}

// Smooth scrolling for anchor links
function addSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
}

// Real-time search/filter functionality (for admin dashboard)
function initializeSearch() {
    const searchInput = document.querySelector('#searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const rows = document.querySelectorAll('tbody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            });
        });
    }
}

// Initialize search on page load
initializeSearch();

// Handle sidebar toggle for mobile
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.classList.toggle('active');
    }
}

// Add mobile menu button functionality
const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', toggleSidebar);
}

// Auto-hide alerts after 5 seconds
const alerts = document.querySelectorAll('.alert');
alerts.forEach(alert => {
    setTimeout(() => {
        alert.style.transition = 'opacity 0.5s';
        alert.style.opacity = '0';
        setTimeout(() => {
            alert.remove();
        }, 500);
    }, 5000);
});

// Format phone numbers as user types
const phoneInputs = document.querySelectorAll('input[type="tel"]');
phoneInputs.forEach(input => {
    input.addEventListener('input', function() {
        let value = this.value.replace(/\D/g, '');
        if (value.length > 10) {
            value = value.substr(0, 10);
        }
        this.value = value;
    });
});

// Password strength indicator
const passwordInputs = document.querySelectorAll('input[type="password"]');
passwordInputs.forEach(input => {
    input.addEventListener('input', function() {
        const strength = getPasswordStrength(this.value);
        updatePasswordStrengthIndicator(this, strength);
    });
});

function getPasswordStrength(password) {
    let strength = 0;
    if (password.length >= 6) strength++;
    if (password.length >= 10) strength++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
    if (/\d/.test(password)) strength++;
    if (/[^a-zA-Z\d]/.test(password)) strength++;
    return strength;
}

function updatePasswordStrengthIndicator(input, strength) {
    let indicator = input.parentElement.querySelector('.password-strength');
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.className = 'password-strength';
        indicator.style.cssText = `
            height: 4px;
            margin-top: 5px;
            border-radius: 2px;
            transition: all 0.3s;
        `;
        input.parentElement.appendChild(indicator);
    }
    
    const colors = ['#f44336', '#ff9800', '#ffeb3b', '#8bc34a', '#4caf50'];
    const widths = ['20%', '40%', '60%', '80%', '100%'];
    
    indicator.style.backgroundColor = colors[strength - 1] || '#f44336';
    indicator.style.width = widths[strength - 1] || '0';
}

// Export functions for use in Django templates
window.BloodBridge = {
    validateForm,
    showNotification,
    acceptBloodRequest,
    updateAvailability,
    toggleSidebar
};
