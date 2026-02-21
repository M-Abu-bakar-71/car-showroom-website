// General JavaScript for the car showroom website

document.addEventListener('DOMContentLoaded', function() {
    // Hamburger Menu Toggle
    const hamburgerMenu = document.getElementById('hamburgerMenu');
    const mobileMenu = document.getElementById('mobileMenu');
    
    if (hamburgerMenu && mobileMenu) {
        hamburgerMenu.addEventListener('click', function() {
            this.classList.toggle('active');
            mobileMenu.classList.toggle('active');
            
            // Toggle body scroll when menu is open
            document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
        });
        
        // Close mobile menu when clicking on links
        const mobileLinks = mobileMenu.querySelectorAll('.nav-link');
        mobileLinks.forEach(link => {
            link.addEventListener('click', () => {
                hamburgerMenu.classList.remove('active');
                mobileMenu.classList.remove('active');
                document.body.style.overflow = '';
            });
        });
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!hamburgerMenu.contains(event.target) && !mobileMenu.contains(event.target)) {
                hamburgerMenu.classList.remove('active');
                mobileMenu.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    }
    
    // Animated Hero Background
    const heroSlides = document.querySelectorAll('.hero-slide');
    if (heroSlides.length > 0) {
        let currentSlide = 0;
        
        function showSlide(n) {
            heroSlides.forEach(slide => slide.classList.remove('active'));
            currentSlide = (n + heroSlides.length) % heroSlides.length;
            heroSlides[currentSlide].classList.add('active');
        }
        
        // Auto-rotate slides every 5 seconds
        setInterval(() => {
            showSlide(currentSlide + 1);
        }, 5000);
        
        // Initialize first slide
        showSlide(0);
    }
    
    // Update order status in admin panel
    const statusBadges = document.querySelectorAll('.status-badge');
    
    statusBadges.forEach(badge => {
        badge.addEventListener('click', function() {
            if (!this.classList.contains('editable')) return;
            
            const orderId = this.getAttribute('data-order-id');
            const currentStatus = this.textContent.trim();
            
            // Show status selection modal or dropdown
            const newStatus = prompt('Enter new status (Pending, Confirmed, Delivered, Cancelled):', currentStatus);
            
            if (newStatus && newStatus !== currentStatus) {
                if (['Pending', 'Confirmed', 'Delivered', 'Cancelled'].includes(newStatus)) {
                    // Show loading
                    this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span>';
                    
                    // Send AJAX request to update status
                    fetch(`/admin/orders/${orderId}/update_status`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                        },
                        body: `status=${encodeURIComponent(newStatus)}`
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            this.textContent = newStatus;
                            updateBadgeColor(this, newStatus);
                            showAlert('Order status updated successfully!', 'success');
                        } else {
                            throw new Error(data.error || 'Failed to update status');
                        }
                    })
                    .catch(error => {
                        console.error('Error updating order status:', error);
                        this.textContent = currentStatus;
                        updateBadgeColor(this, currentStatus);
                        showAlert('Error updating order status: ' + error.message, 'danger');
                    });
                } else {
                    alert('Invalid status. Please use: Pending, Confirmed, Delivered, or Cancelled');
                }
            }
        });
    });
    
    // Image loading error handler
    const carImages = document.querySelectorAll('.car-image, .car-detail-image');
    
    carImages.forEach(img => {
        img.addEventListener('error', function() {
            this.src = 'https://images.unsplash.com/photo-1563720223485-85756d06134f?w=500&h=300&fit=crop';
            this.alt = 'Car image not available';
        });
    });
    
    // Form validation enhancements
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Processing...';
                submitBtn.disabled = true;
            }
        });
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Price formatting
    const priceElements = document.querySelectorAll('.price-tag');
    priceElements.forEach(element => {
        const price = parseFloat(element.textContent.replace(/[^0-9.-]+/g, ""));
        if (!isNaN(price)) {
            element.textContent = formatPrice(price);
        }
    });
});

function updateBadgeColor(badge, status) {
    badge.className = 'badge status-badge editable';
    if (status === 'Pending') {
        badge.classList.add('bg-warning');
    } else if (status === 'Confirmed') {
        badge.classList.add('bg-primary');
    } else if (status === 'Delivered') {
        badge.classList.add('bg-success');
    } else {
        badge.classList.add('bg-danger');
    }
}

function formatPrice(price) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(price);
}

function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show slide-in-left`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at the top of the container
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentElement) {
                alertDiv.remove();
            }
        }, 5000);
    }
}