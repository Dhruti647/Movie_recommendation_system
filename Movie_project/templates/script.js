function validate()
{
    var email = document.getElementBYID("email").value;
    var password= document.getElementBYID("password").value;
    if((email=="admin") && password=="user")
    {
        alert("login successfully");
        return false;
    }

    else{
        alert("login failed");
    }
}