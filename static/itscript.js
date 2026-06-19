


const API_URL = "http://localhost:8000/api/it/tickets";
// const API_URL = "http://localhost:8000/api/tickets";

function showFormMessage(text, type = "success") {
  const el = document.getElementById("formMessage");
  el.innerHTML = text;
  el.className = `message ${type}`;
  el.classList.remove("hidden");
}

// STRICT .com and .in ONLY validation
function validateEmail(email) {
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|in)$/i;
  
  if (!emailRegex.test(email)) {
    return { 
      valid: false, 
      message: 'Please use .com or .in domains only (e.g., name@gmail.com, name@jhs.co.in)' 
    };
  }
  
  return { valid: true };
}

function validatePhone(phone) {
  const phoneRegex = /^[6-9]\d{9}$/; // Indian 10-digit starting 6-9
  return phoneRegex.test(phone) ? { valid: true } : 
         { valid: false, message: 'Enter valid 10-digit mobile (starts with 6-9)' };
}

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("ticketForm");
  const emailInput = document.getElementById("email");
  const phoneInput = document.getElementById("phone");
  const emailError = document.getElementById("emailError") || document.createElement("span");

  // Create error span if doesn't exist
  if (!document.getElementById("emailError")) {
    emailError.id = "emailError";
    emailError.className = "error-message";
    emailInput.parentNode.appendChild(emailError);
  }

  // Real-time email validation (.com/.in only)
  emailInput.addEventListener('input', function(e) {
    const email = e.target.value.trim();
    const validation = validateEmail(email);
    
    if (email) {
      if (validation.valid) {
        e.target.setCustomValidity('');
        emailError.textContent = '';
        e.target.classList.remove('invalid');
        e.target.classList.add('valid');
      } else {
        e.target.setCustomValidity(validation.message);
        emailError.textContent = validation.message;
        e.target.classList.add('invalid');
        e.target.classList.remove('valid');
      }
    } else {
      e.target.setCustomValidity('');
      emailError.textContent = '';
    }
  });

  // Real-time phone validation
  phoneInput.addEventListener('input', function(e) {
    const phone = e.target.value.trim();
    if (phone && !validatePhone(phone).valid) {
      e.target.setCustomValidity(validatePhone(phone).message);
    } else {
      e.target.setCustomValidity('');
    }
  });

  // Form submission with full validation
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Get all values
    const email = document.getElementById("email").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const name = document.getElementById("name").value.trim();
    const issueDesc = document.getElementById("issueDescription").value.trim();
    const reportingPartner = document.getElementById("reportingPartner").value;

    // Email validation (.com/.in ONLY)
    const emailValidation = validateEmail(email);
    if (!emailValidation.valid || !email) {
      showFormMessage(emailValidation.valid ? "Email is required." : emailValidation.message, "error");
      document.getElementById("email").focus();
      return;
    }

    // Phone validation
    if (!phone) {
      showFormMessage("Phone number is required.", "error");
      document.getElementById("phone").focus();
      return;
    }
    const phoneValidation = validatePhone(phone);
    if (!phoneValidation.valid) {
      showFormMessage(phoneValidation.message, "error");
      document.getElementById("phone").focus();
      return;
    }

    // Name validation
    if (!name || name.length < 2) {
      showFormMessage("Please enter valid full name (minimum 2 characters).", "error");
      document.getElementById("name").focus();
      return;
    }

    // Issue description
    if (!issueDesc || issueDesc.length < 10) {
      showFormMessage("Please provide detailed issue description (minimum 10 characters).", "error");
      document.getElementById("issueDescription").focus();
      return;
    }

    // Issues checkboxes
    const issuesChecked = Array.from(
      document.querySelectorAll('input[name="issues"]:checked')
    ).map(i => i.value);

    const otherChecked = document.getElementById("issueOtherChk")?.checked;
    const otherText = document.getElementById("issueOtherText")?.value.trim();
    if (otherChecked && otherText) {
      issuesChecked.push(`Other: ${otherText}`);
    }

    if (issuesChecked.length === 0) {
      showFormMessage("Please select at least one IT issue.", "error");
      return;
    }

    // Reporting partner
    if (!reportingPartner) {
      showFormMessage("Please select Reporting Partner.", "error");
      return;
    }

    // Prepare payload
    const payload = {
      name: name,
      email: email,
      phone: phone,
      assetCode: document.getElementById("assetCode").value.trim(),
      issues: issuesChecked,
      issueDescription: issueDesc,
      reportingPartner: reportingPartner
    };

    // Loading state
    const submitBtn = form.querySelector('.btn-primary');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = 'Creating Ticket...';
    submitBtn.disabled = true;

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const data = await res.json();

      if (!res.ok) {
        if (res.status === 422) {
          // FastAPI validation errors
          const errors = data.detail.map(err => err.msg).join(', ');
          throw new Error(`Validation Error: ${errors}`);
        }
        throw new Error(data.detail || "Failed to create ticket");
      }

      // Success!
      showFormMessage(
        `Ticket created successfully!<br><strong>Ticket ID: ${data.id}</strong><br>Check your email for confirmation!`,
        "success"
      );
      form.reset();
      
      // Clear validation states
      emailInput.classList.remove('valid', 'invalid');
      phoneInput.classList.remove('valid', 'invalid');
      emailError.textContent = '';
      
    } catch (err) {
      console.error('Error:', err);
      showFormMessage(err.message || "Something went wrong. Please try again.", "error");
    } finally {
      // Reset button
      submitBtn.innerHTML = originalText;
      submitBtn.disabled = false;
    }
  });
});
