



// API endpoints for both HR and IT
const API_ENDPOINTS = {
    hr: '/api/admin',
    it: '/api/admin'
};

// Redirect URLs after successful login
const REDIRECT_URLS = {
    hr: '/admin',
    it: '/it-admin'
};

function showMessage(message, type = 'success') {
    const msgEl = document.getElementById('loginMessage');
    msgEl.innerHTML = message;
    msgEl.className = `message ${type}`;
    msgEl.classList.remove('hidden');
    
    setTimeout(() => {
        msgEl.classList.add('hidden');
    }, 5000);
}

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('loginForm');
    const empCodeInput = document.getElementById('empCode');
    const helpdeskTypeSelect = document.getElementById('helpdeskType');
    
    // Auto-uppercase employee code
    empCodeInput.addEventListener('input', (e) => {
        e.target.value = e.target.value.toUpperCase().replace(/[^A-Z0-9]/g, '');
    });
    
    // Change title text only (no emoji), keep SVG icon intact
    helpdeskTypeSelect.addEventListener('change', (e) => {
        const titleEl = document.getElementById('logoTitle');
        if (e.target.value === 'hr') {
            titleEl.textContent = 'JHS HR Admin';
        } else if (e.target.value === 'it') {
            titleEl.textContent = 'JHS IT Admin';
        } else {
            titleEl.textContent = 'JHS Admin Portal';
        }
    });
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalHTML = submitBtn.innerHTML;
        submitBtn.innerHTML = '<span class="btn-loading">Logging in...</span>';
        submitBtn.disabled = true;
        
        const helpdeskType = document.getElementById('helpdeskType').value;
        const empCode = document.getElementById('empCode').value.trim().toUpperCase();
        const password = document.getElementById('password').value;
        
        if (!helpdeskType) {
            showMessage('Please select a helpdesk type', 'error');
            submitBtn.innerHTML = originalHTML;
            submitBtn.disabled = false;
            return;
        }
        
        if (!empCode || !password) {
            showMessage('Employee Code and Password required', 'error');
            submitBtn.innerHTML = originalHTML;
            submitBtn.disabled = false;
            return;
        }
        
        const formData = { empCode, password };
        
        try {
            console.log(`Attempting ${helpdeskType.toUpperCase()} login for:`, empCode);
            
            const apiEndpoint = API_ENDPOINTS[helpdeskType];
            const response = await fetch(`${apiEndpoint}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.detail || 'Login failed');
            }
            
            if (helpdeskType === 'hr') {
                localStorage.setItem('adminToken', result.access_token || result.token);
                localStorage.setItem('adminName', result.name);
                localStorage.setItem('adminEmpCode', empCode);
                localStorage.setItem('helpdeskType', 'hr');
            } else if (helpdeskType === 'it') {
                localStorage.setItem('adminLoggedIn', 'true');
                localStorage.setItem('adminEmpCode', result.empCode || empCode);
                localStorage.setItem('jwtToken', result.token || result.access_token);
                localStorage.setItem('helpdeskType', 'it');
            }
            
            showMessage('Login successful! Redirecting...', 'success');
            
            setTimeout(() => {
                window.location.href = REDIRECT_URLS[helpdeskType];
            }, 500);
            
        } catch (error) {
            console.error('Login error:', error);
            showMessage(error.message, 'error');
        } finally {
            submitBtn.innerHTML = originalHTML;
            submitBtn.disabled = false;
        }
    });
});