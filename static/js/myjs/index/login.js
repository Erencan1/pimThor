function post(data) {
    data['csrfmiddlewaretoken'] = cf;
    return JSON.parse($.ajax({
        type: "POST",
        data: data,
        async: false
    }).responseText);
}


var form = document.forms[0];
var button = document.getElementById('sbmt');
var username = document.getElementById('username');
var password = document.getElementById('password');
var passwor_l = 8;
var passwor_h = 30;
var fgt = document.getElementById('forgot');
var signup = document.getElementById('signup');

var cf = document.getElementsByName('csrfmiddlewaretoken')[0].value;

signup.onclick = function ()
{
    removeElemnt(this.parentNode);
    username.setAttribute('name', 'new' + username.name);
    password.setAttribute('name', 'a' + password.name);
    var email = document.createElement("INPUT");
    email.setAttribute("type", "email");
    email.setAttribute('name', 'newemail');
    email.placeholder = 'email';
    email.required = true;
    password.parentNode.insertBefore(email, password);
    button.innerHTML = 'Sign UP'
};
fgt.onclick = function ()
{
    removeElemnt(this.parentNode);
    removeElemnt(password);
    username.placeholder = 'Enter username or email';
    button.innerHTML = 'Send me the unique code by e-mail';
    button.onclick = function ()
    {
        if (username.value.includes('@'))
        {
            alert('username can not contain @');
            username.value = '';
            return false
        }
        button.disabled = true;
        var respons = post({'username': username.value});
        alert(respons['message']);
        if (!respons['status']){
            button.disabled = false;
            return false;
        }
        username.value = '';
        username.placeholder = 'Enter the unique code';
        username.setAttribute('name', 'uniqueCode');
        button.innerHTML = 'Submit';
        var cap = respons['cap'];
        button.disabled = false;
        button.onclick = function ()
        {
            button.disabled = true;
            var respons = post({'uniqueCode': cap+'_'+username.value});
            if (!respons['status'])
            {
                alert(respons['message']);
                button.disabled = false;
                return false;
            }
            password.value = '';
            password.placeholder = 'Enter new password';
            password.setAttribute('name', 'newpassword');
            button.innerHTML = 'Update the Password';

            username.parentNode.replaceChild(password, username);

            button.disabled = false;
            button.onclick = function ()
            {
                button.disabled = false;
                password.hidden = true;
                password.value = cap+'_'+password.value+'_'+username.value;
                passwor_l += username.value.length + 1;
                passwor_h += username.value.length + 1;
            }
        }

    }
};
function removeElemnt(element)
{
    element.parentNode.removeChild(element);
}
form.onsubmit = function ()
{
    if (password.value.length >= passwor_l && password.value.length < passwor_h)
    {
        return true;
    }
    alert('The password must be between 8 and 30 characters.');
    password.value = '';
    password.style.backgroundColor = 'red';
    password.hidden = false;
    return false;
};