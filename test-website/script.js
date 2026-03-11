document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contact-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            const data = Object.fromEntries(formData);
            
            console.log('Form data:', data);
            
            const successMessage = document.createElement('div');
            successMessage.className = 'success-message';
            successMessage.textContent = 'Form submitted successfully!';
            successMessage.style.cssText = `
                background: #10b981;
                color: white;
                padding: 1rem;
                border-radius: 4px;
                margin-top: 1rem;
                text-align: center;
            `;
            
            form.parentNode.insertBefore(successMessage, form.nextSibling);
            
            setTimeout(() => {
                successMessage.remove();
            }, 3000);
            
            form.reset();
        });
    }
});