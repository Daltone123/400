// document.addEventListener("DOMContentLoaded", function () {
//   const form = document.getElementById("signup-form");
//   const btn = document.getElementById("signup-btn");

//   form.addEventListener("submit", async function (event) {
//       event.preventDefault();

//       const firstName = document.getElementById("signup-first-name").value.trim();
//       const lastName = document.getElementById("signup-last-name").value.trim();
//       const email = document.getElementById("signup-email").value.trim();
//       const password = document.getElementById("signup-password").value.trim();

//       if (!firstName || !lastName || !email || !password) {
//           createToast("All fields are required.", -1);
//           return;
//       }

//       btn.disabled = true;

//       try {
//           const response = await fetch("/signup/", {
//               method: "POST",
//               headers: { "Content-Type": "application/json", "X-CSRFToken": getCSRFToken() },
//               body: JSON.stringify({ first_name: firstName, last_name: lastName, email, password }),
//           });

//           const data = await response.json();

//           if (response.ok) {
//               createToast(data.message, "success");
//               setTimeout(() => window.location.href = "/login/", 2000);
//           } else {
//               createToast(data.error || "Signup failed. Try again.", "error");
//           }
//       } catch (error) {
//           createToast("Network error. Please try again.", "error");
//       } finally {
//           btn.disabled = false;
//       }
//   });
// });

// // Function to get CSRF token
// function getCSRFToken() {
//   return document.querySelector("[name=csrfmiddlewaretoken]").value;
// }

$(document).ready(function(){
    //Login js
    $("#login-form").submit(function(event){
        event.preventDefault();
        const loginBtn = document.getElementById("login-btn");
        // const loginSpinner = document.getElementById("login-spinner");

        const email = document.getElementById("login-email").value.trim();
        const password = document.getElementById("login-password").value.trim();
        if (!email || !password) {
            createToast("All fields are required.", -1);
            return;
        }
        loginBtn.disabled = true;
        // loginSpinner.style.display = "block";
        const formData = new FormData(this);
        fetch("/login/", {
            method:'POST',
            body: formData
        }).then(response=>{
            if(!response.ok){
                createToast("Something went wrong", -1);
                throw new Error("Error occured!");
            }
            return response.json();
        }).then(data=>{
            const message = data.message;
            const status = data.status;
            createToast(message, 200);
            if(status == 200){
                window.location.href = "/";
            }
        }).catch(error=>{
            createToast("Error"+error, -1);
        }).finally(()=>{
            loginBtn.disabled = false;
            // loginSpinner.style.display = "none";
        });
    });

    // sign up js
    
});
