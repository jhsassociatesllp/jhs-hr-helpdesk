// // const API_ADMIN = 'http://localhost:8000/api/admin';
// const API_ADMIN = '/api/admin';

// function showMessage(message, type = 'success') {
//     const msgEl = document.getElementById('loginMessage');
//     msgEl.innerHTML = message;
//     msgEl.className = `message ${type}`;
//     msgEl.classList.remove('hidden');
// }

// document.addEventListener('DOMContentLoaded', () => {
//     const form = document.getElementById('loginForm');
    
//     const empCodeInput = document.getElementById('empCode');
//     empCodeInput.addEventListener('input', (e) => {
//         e.target.value = e.target.value.toUpperCase().replace(/[^A-Z0-9]/g, '');
//     });
    
//     form.addEventListener('submit', async (e) => {
//         e.preventDefault();
        
//         const submitBtn = form.querySelector('button[type="submit"]');
//         const originalText = submitBtn.innerHTML;
//         submitBtn.innerHTML = '<span class="btn-loading">⏳ Logging in...</span>';
//         submitBtn.disabled = true;
        
//         const formData = {
//             empCode: document.getElementById('empCode').value.trim().toUpperCase(),
//             password: document.getElementById('password').value
//         };
        
//         if (!formData.empCode || !formData.password) {
//             showMessage('❌ Employee Code and Password required', 'error');
//             submitBtn.innerHTML = originalText;
//             submitBtn.disabled = false;
//             return;
//         }
        
//         try {
//             console.log("sending login request")
//             const response = await fetch(`${API_ADMIN}/login`, {
//                 method: 'POST',
//                 headers: { 'Content-Type': 'application/json' },
//                 body: JSON.stringify(formData)
//             });
            
//             const result = await response.json();
            
//             if (!response.ok) {
//                 throw new Error(result.detail || 'Login failed');
//             }
            
//             localStorage.setItem('adminLoggedIn', 'true');
//             localStorage.setItem('adminEmpCode', formData.empCode);
//             window.location.href = 'admin.html';
            
//         } catch (error) {
//             console.error('Login error:', error);
//             showMessage(`❌ ${error.message}`, 'error');
//         } finally {
//             submitBtn.innerHTML = originalText;
//             submitBtn.disabled = false;
//         }
//     });
// });




// // const API_ADMIN = 'http://localhost:8000/api/admin';
// const API_ADMIN = '/api/admin';

// function showMessage(message, type = 'success') {
//     const msgEl = document.getElementById('loginMessage');
//     msgEl.innerHTML = message;
//     msgEl.className = `message ${type}`;
//     msgEl.classList.remove('hidden');
// }

// document.addEventListener('DOMContentLoaded', () => {
//     const form = document.getElementById('loginForm');
    
//     const empCodeInput = document.getElementById('empCode');
//     empCodeInput.addEventListener('input', (e) => {
//         e.target.value = e.target.value.toUpperCase().replace(/[^A-Z0-9]/g, '');
//     });
    
//     // Password visibility toggle
//     const togglePassword = document.getElementById('togglePassword');
//     const passwordInput = document.getElementById('password');
    
//     togglePassword.addEventListener('click', () => {
//         const type = passwordInput.type === 'password' ? 'text' : 'password';
//         passwordInput.type = type;
        
//         // Toggle eye icon
//         const eyeIcon = togglePassword.querySelector('.eye-icon');
//         eyeIcon.textContent = type === 'password' ? '👁️' : '👁️‍🗨️';
//     });
    
//     form.addEventListener('submit', async (e) => {
//         e.preventDefault();
        
//         const submitBtn = form.querySelector('button[type="submit"]');
//         const originalText = submitBtn.innerHTML;
//         submitBtn.innerHTML = '<span class="btn-loading">⏳ Logging in...</span>';
//         submitBtn.disabled = true;
        
//         const formData = {
//             empCode: document.getElementById('empCode').value.trim().toUpperCase(),
//             password: document.getElementById('password').value
//         };
        
//         if (!formData.empCode || !formData.password) {
//             showMessage('❌ Employee Code and Password required', 'error');
//             submitBtn.innerHTML = originalText;
//             submitBtn.disabled = false;
//             return;
//         }
        
//         try {
//             console.log("sending login request")
//             const response = await fetch(`${API_ADMIN}/login`, {
//                 method: 'POST',
//                 headers: { 'Content-Type': 'application/json' },
//                 body: JSON.stringify(formData)
//             });
            
//             const result = await response.json();
            
//             if (!response.ok) {
//                 throw new Error(result.detail || 'Login failed');
//             }
            
//             localStorage.setItem('adminLoggedIn', 'true');
//             localStorage.setItem('adminEmpCode', formData.empCode);
//             window.location.href = 'admin.html';
            
//         } catch (error) {
//             console.error('Login error:', error);
//             showMessage(`❌ ${error.message}`, 'error');
//         } finally {
//             submitBtn.innerHTML = originalText;
//             submitBtn.disabled = false;
//         }
//     });
// });





// const API_ADMIN = 'http://localhost:8000/api/admin';
const API_ADMIN = '/api/admin';

function showMessage(message, type = 'success') {
    const msgEl = document.getElementById('loginMessage');
    msgEl.innerHTML = message;
    msgEl.className = `message ${type}`;
    msgEl.classList.remove('hidden');
}

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('loginForm');
    
    const empCodeInput = document.getElementById('empCode');
    empCodeInput.addEventListener('input', (e) => {
        e.target.value = e.target.value.toUpperCase().replace(/[^A-Z0-9]/g, '');
    });
    
    // Password visibility toggle
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('password');
    
    togglePassword.addEventListener('click', () => {
        const type = passwordInput.type === 'password' ? 'text' : 'password';
        passwordInput.type = type;
        
        // Toggle eye icon
        togglePassword.classList.toggle('show-password');
    });
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<span class="btn-loading">⏳ Logging in...</span>';
        submitBtn.disabled = true;
        
        const formData = {
            empCode: document.getElementById('empCode').value.trim().toUpperCase(),
            password: document.getElementById('password').value
        };
        
        if (!formData.empCode || !formData.password) {
            showMessage('❌ Employee Code and Password required', 'error');
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
            return;
        }
        
        try {
            console.log("sending login request")
            const response = await fetch(`${API_ADMIN}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.detail || 'Login failed');
            }
            
            localStorage.setItem('adminLoggedIn', 'true');
            localStorage.setItem('adminEmpCode', formData.empCode);
            window.location.href = 'admin.html';
            
        } catch (error) {
            console.error('Login error:', error);
            showMessage(`❌ ${error.message}`, 'error');
        } finally {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    });
});