const buttons = document.querySelectorAll('.btn');

buttons.forEach(button => button.addEventListener('click', event => {
    fetch('/pay')
    .then(result => { return result.json(); })
    .then(data => {
        var stripe = Stripe(data.checkout_public_key);

        stripe.redirectToCheckout({
            sessionId: data.checkout_session_id
        }).then(result => {})
    })
}));