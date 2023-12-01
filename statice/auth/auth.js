/* Global variables */

let currentForm = true;
let forms = document.getElementsByClassName("form");
let switchText = document.getElementById("switch-text");

/* Events */

// Init
window.onload = function() 
{
    switchForms();
};



/* Utilities */

function switchForms()
{
    console.log(forms);
    if(currentForm)
    {
        switchText.innerHTML = "Don't have an account? <span class = 'link-mockup'>sign up</span>";
    }
    else
    {
        switchText.innerHTML = "Already have an account? <span class = 'link-mockup'>login</span>";
    }

    forms[+currentForm].style.display = "none";
    currentForm = !currentForm;
    forms[+currentForm].style.display = "unset";
}

function validateConfirmPassword()
{
    let passwordInput = document.getElementById("passwordInput");
    let confirmPasswordInput = document.getElementById("confirmPasswordInput");

    if(confirmPasswordInput.value === passwordInput.value && isEmpty(confirmPasswordInput.value) === false && isEmpty(passwordInput.value) === false)
    {
        let signUpButton = document.getElementById("sign-up-submit")
        signUpButton.type = "submit";
        confirmPasswordInput.style.color = "black";
        document.getElementById("confirmPasswordLabel").style.color = "rgb(70, 208, 183)";
    }
    else
    {
        let signUpButton = document.getElementById("sign-up-submit")
        signUpButton.type = "button";
        confirmPasswordInput.style.color = "red";
        document.getElementById("confirmPasswordLabel").style.color = "red";
    }
}

function isEmpty(str) 
{
    return !str.trim().length;
}