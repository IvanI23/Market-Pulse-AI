function showSignupModal(message, tickers) {
    document.getElementById('signupMessage').textContent = message;
    document.getElementById('signupTickers').textContent = tickers;
    document.getElementById('signupModal').style.display = 'block';
}

function showUnsubscribeModal(message) {
    document.getElementById('unsubscribeMessage').textContent = message;
    document.getElementById('unsubscribeModal').style.display = 'block';
}

function closeSignupModal() {
    document.getElementById('signupModal').style.display = 'none';
}

function closeUnsubscribeModal() {
    document.getElementById('unsubscribeModal').style.display = 'none';
}

function initializeListeners() {
    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('modal')) {
            closeSignupModal();
            closeUnsubscribeModal();
        }
        
        if (event.target.classList.contains('close')) {
            closeSignupModal();
            closeUnsubscribeModal();
        }
    });

    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeSignupModal();
            closeUnsubscribeModal();
        }
    });
}

function showModalOnLoad(type, message, tickers) {
    document.addEventListener('DOMContentLoaded', function() {
        initializeListeners();
        
        if (type === 'signup') {
            showSignupModal(message, tickers);
        } else if (type === 'unsubscribe') {
            showUnsubscribeModal(message);
        }
    });
}
