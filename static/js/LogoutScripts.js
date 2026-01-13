document.getElementById('confirm-logout').addEventListener('click', function () {
    window.location.href = '../templates/landing.html'; // Redirect to the logout page

});


document.getElementById('cancel-logout').addEventListener('click', function () {
    
    window.history.back(); 
});