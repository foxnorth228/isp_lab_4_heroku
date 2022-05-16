console.log(document.getElementById('submitForm'))
console.log(document.getElementById('submit'))
const form = document.getElementById('submitForm');
form.addEventListener('submit', function(e) {
    const username = form.getElementById('id_username');
    console.log(username, username.value, (username.value).match(/[^a-zA-Z0-9@.+-_]{1-150}/))
    if((username.value).match(/[^a-zA-Z0-9@.+-_]{1-150}/) === null) {
        e.submit();
    }
    e.preventDefault();
    e.stopPropagation();
    console.log("Clicked")
})