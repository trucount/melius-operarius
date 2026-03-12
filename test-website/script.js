document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contact-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            const data = Object.fromEntries(formData);
            
            console.log('Form data:', data);
            
            const submitButton = form.querySelector('button');
            const originalText = submitButton.textContent;
            submitButton.textContent = 'Submitting...';
            submitButton.disabled = true;
            
            fetch(form.action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                
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
            })
            .catch(error => {
                console.error('Error:', error);
                
                const errorMessage = document.createElement('div');
                errorMessage.className = 'error-message';
                errorMessage.textContent = 'Error submitting form. Please try again.';
                errorMessage.style.cssText = `
                    background: #ef4444;
                    color: white;
                    padding: 1rem;
                    border-radius: 4px;
                    margin-top: 1rem;
                    text-align: center;
                `;
                
                form.parentNode.insertBefore(errorMessage, form.nextSibling);
                
                setTimeout(() => {
                    errorMessage.remove();
                }, 3000);
            })
            .finally(() => {
                submitButton.textContent = originalText;
                submitButton.disabled = false;
            });
        });
    }
});