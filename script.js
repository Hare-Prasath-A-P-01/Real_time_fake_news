const wrapper = document.querySelector('.wrapper');
const signUpLink = document.querySelector('.signUp-link');
const signInLink = document.querySelector('.signIn-link');

signUpLink.addEventListener('click', () => {
    wrapper.classList.add('animate-signIn');
    wrapper.classList.remove('animate-signUp');
});

signInLink.addEventListener('click', () => {
    wrapper.classList.add('animate-signUp');
    wrapper.classList.remove('animate-signIn');
});

document.addEventListener("DOMContentLoaded", function () {
    // Sign-up form event listener
    document.querySelector(".sign-up form").addEventListener("submit", async function (event) {
        event.preventDefault();

        let username = this.querySelector("input[type='text']").value;
        let email = this.querySelector("input[type='email']").value;
        let password = this.querySelector("input[type='password']").value;

        try {
            const response = await fetch("http://localhost:5000/signup", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, email, password })
            });

            const data = await response.json();
            alert(data.message);
        } catch (error) {
            console.error("Error:", error);
        }
    });

    // Sign-in form event listener (with Streamlit redirection)
    document.querySelector(".sign-in form").addEventListener("submit", async function (event) {
        event.preventDefault();

        let username = this.querySelector("input[type='text']").value;
        let password = this.querySelector("input[type='password']").value;

        try {
            const response = await fetch("http://localhost:5000/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();
            
            if (response.ok) {
                alert(data.message);
                window.location.href = data.redirectURL; // Redirect to Streamlit app
            } else {
                alert(data.message);
            }
        } catch (error) {
            console.error("Error:", error);
        }
    });
});
