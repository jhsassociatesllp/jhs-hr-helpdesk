


// ========== CONFIG ==========
// const API_URL = 'http://localhost:8000/api/tickets';
const API_URL = '/api/tickets';

// ========== FORM VALIDATION ==========
function validateForm(formData) {
    const errors = [];
    
    // Name validation
    if (!formData.name.trim()) {
        errors.push('Name is required');
    } else if (formData.name.trim().length < 2) {
        errors.push('Name must be at least 2 characters');
    }
    
    // Employee Code validation (JHS + exactly 4 digits)
    // if (!formData.empCode.trim()) {
    //     errors.push('Employee code is required');
    // } else if (!/^JHS\d{4}$/.test(formData.empCode.trim().toUpperCase())) {
    //     errors.push('Employee code must be in format JHS0001');
    // }

    // Employee Code validation (optional, but if filled must start with JHS)
    if (formData.empCode.trim()) { 
    if (!/^JHS/.test(formData.empCode.trim().toUpperCase())) {
        errors.push('Employee code must start with JHS');
     }
     }

    
    // Email validation (.com or .in only)
    if (!formData.email.trim()) {
        errors.push('Email is required');
    } else if (!/^[^\s@]+@[^.\s]+\.(com|in)$/i.test(formData.email.trim())) {
        errors.push('Email must end with .com or .in');
    }
    
    // Phone validation (exactly 10 digits)
    if (!formData.phone.trim()) {
        errors.push('Phone number is required');
    } else if (!/^\d{10}$/.test(formData.phone.trim())) {
        errors.push('Phone must be exactly 10 digits');
    }
    
    // Category validation
    if (!formData.category) {
        errors.push('Category is required');
    }
    
    // Issue validation
    if (!formData.issue.trim()) {
        errors.push('Issue description is required');
    } else if (formData.issue.trim().length < 10) {
        errors.push('Issue description must be at least 10 characters');
    }
    
    return errors;
}

// ========== SHOW MESSAGE ==========
function showMessage(message, type = 'success') {
    const msgEl = document.getElementById('formMessage');
    msgEl.innerHTML = message;
    msgEl.className = `message ${type}`;
    msgEl.style.display = 'block';
    
    if (type === 'success') {
        // Auto-hide success after 5s
        setTimeout(() => {
            msgEl.style.display = 'none';
        }, 5000);
    }
}

// ========== MAIN FORM SUBMISSION ==========
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('ticketForm');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Show loading
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '⏳ Submitting...';
        submitBtn.disabled = true;
        
        // Collect form data
        const formData = {
            name: document.getElementById('name').value.trim(),
            email: document.getElementById('email').value.trim(),
            phone: document.getElementById('phone').value.trim(),
            empCode: document.getElementById('empCode').value.trim().toUpperCase(),
            category: document.getElementById('category').value,
            issue: document.getElementById('issue').value.trim()
        };
        
        // Validate ALL fields
        const errors = validateForm(formData);
        if (errors.length > 0) {
            showMessage('❌ ' + errors.join('<br>'), 'error');
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
            return;
        }
        
        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.detail || 'Submission failed');
            }
                 

            // Success!
            showMessage(
                `🎉 Ticket created successfully!<br>` +
                `<strong>Ticket ID: ${result.ticketId}</strong><br>` +
                `📧 Check your email for confirmation. HR will contact you soon!`, 
                'success'
            );
            
            // Reset form
            form.reset();
            
        } catch (error) {
            console.error('Submission error:', error);
            let errorMsg = 'Failed to create ticket';
            
            if (error.message.includes('Network')) {
                errorMsg = '❌ No connection to server. Please check if backend is running.';
            } else if (error.message.includes('CORS')) {
                errorMsg = '❌ Server configuration issue. Check FastAPI CORS settings.';
            } else {
                errorMsg += ': ' + error.message;
            }
            
            showMessage(errorMsg, 'error');
        } finally {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    });
    
    // Real-time formatting
    const empCodeInput = document.getElementById('empCode');
    if (empCodeInput) {
        empCodeInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.toUpperCase().replace(/[^A-Z0-9]/g, '');
        });
    }
    
    const phoneInput = document.getElementById('phone');
    if (phoneInput) {
        phoneInput.addEventListener('input', (e) => {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 10) {
                value = value.slice(0, 10);
            }
            e.target.value = value;
        });
    }
});


