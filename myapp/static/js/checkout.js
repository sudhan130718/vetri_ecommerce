document.addEventListener("DOMContentLoaded", function () {
    const paymentMethodRadios = document.querySelectorAll('input[name="payment_method"]');
    const cardDetails = document.getElementById('card-details');

    if (paymentMethodRadios && cardDetails) {  // Check if the elements exist
        paymentMethodRadios.forEach(radio => {
            radio.addEventListener('change', function () {
                if (document.getElementById('card').checked) {
                    cardDetails.style.display = 'block';
                } else {
                    cardDetails.style.display = 'none';
                }
            });
        });
    } else {
        console.error("Required elements not found in the DOM.");
    }
});
