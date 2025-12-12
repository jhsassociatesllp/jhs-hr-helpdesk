

// const API_ADMIN = 'http://localhost:8000/api/admin';

const API_ADMIN = '/api/admin';

function showMessage(message, type = 'success') {
    const msgEl = document.getElementById('registerMessage');
    msgEl.innerHTML = message;
    msgEl.className = `message ${type}`;
    msgEl.classList.remove('hidden');
}

function validatePassword(password) {
    if (password.length < 6) return 'Password must be at least 6 characters';
    return null;
}

function validateEmpCode(empCode) {
    const pattern = /^JHS\d{4}$/;
    return pattern.test(empCode);
}

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('registerForm');
    const empCodeInput = document.getElementById('empCode');

    empCodeInput.addEventListener('input', (e) => {
        e.target.value = e.target.value.toUpperCase().replace(/[^A-Z0-9]/g, '');
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<span class="btn-loading">⏳ Registering...</span>';
        submitBtn.disabled = true;

        const name = document.getElementById('name').value.trim();
        const empCode = document.getElementById('empCode').value.trim().toUpperCase();
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;

        let error = null;

        if (!name) {
            error = 'Name is required';
        } else if (!empCode) {
            error = 'Employee code is required';
        } else if (!validateEmpCode(empCode)) {
            error = 'Employee code must be in the format JHS0000';
        } else if (!password) {
            error = 'Password is required';
        } else if (!confirmPassword) {
            error = 'Confirm Password is required';
        } else if (password !== confirmPassword) {
            error = 'Password and Confirm Password do not match';
        } else {
            const pwError = validatePassword(password);
            if (pwError) error = pwError;
        }

        if (error) {
            showMessage(`❌ ${error}`, 'error');
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
            return;
        }

        try {
            const formData = { name, empCode, password };
            const response = await fetch(`${API_ADMIN}/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.detail || 'Registration failed');
            }

            showMessage(
                `🎉 Admin registered successfully!<br><strong>${empCode}</strong><br>You can now <a href="adminlogin.html">login here</a>`,
                'success'
            );
            form.reset();

        } catch (error) {
            console.error('Registration error:', error);
            let errorMsg = error.message;
            if (errorMsg.includes('already exists')) {
                errorMsg = 'Admin with this Employee Code already exists';
            }
            showMessage(`❌ ${errorMsg}`, 'error');
        } finally {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    });
});
