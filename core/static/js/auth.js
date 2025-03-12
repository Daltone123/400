
$(document).ready(function(){
    //Login js
    $("#login-form").submit(function(event){
        event.preventDefault();
        const loginBtn = document.getElementById("login-btn");
        // const loginSpinner = document.getElementById("login-spinner");

        const email = document.getElementById("login-email").value.trim();
        const password = document.getElementById("login-password").value.trim();
        if (!email || !password) {
            alert("All fields are required.");
            return;
        }
        loginBtn.disabled = true;
        // loginSpinner.style.display = "block";
        const formData = new FormData(this);
        fetch("/login", {
            method:'POST',
            body: formData
        }).then(response=>{
            return response.json();
        }).then(data=>{
            const message = data.message;
            const status = data.status;
            if(status == 200){
                window.location.href = "/upload";
            }else{
                alert(message);
            }
        }).catch(error=>{
            console.error(error);
            alert("Error occured");
        }).finally(()=>{
            loginBtn.disabled = false;
            // loginSpinner.style.display = "none";
        });
    });

    // sign up js farmer

    $("#farmer-registration-form").submit(function(event){
        event.preventDefault();
        // const signupSpinner = document.getElementById("signup-spinner")
        const formData = new FormData(this);
        const url = "/signup_f";
        sign_up_user(url, formData);
    });

    // sign up js farmer

    $("#agrovet-registration-form").submit(function(event){
        event.preventDefault();
        // const signupSpinner = document.getElementById("signup-spinner")
        const formData = new FormData(this);
        const url = "/signup_a";
        sign_up_user(url, formData);
    });
    function sign_up_user(url, formData){
        fetch(url, {
            method: "POST",
            body: formData
        }).then(response=>{
            return response.json();
        }).then(data=>{
            const message= data.message
            const status = data.status;

            if (status == 200||status == 201){
                alert(message);
                window.location.href = "/login";
            }else{
                alert(message);
            }
        }).catch(error=>{
            console.error(error);
            alert("Something went wrong. Please try again");
        })
    }
    // sign up js buyer
    
});
