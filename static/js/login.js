document.getElementById("loginForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("/api/login/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok && data.status === "success") {
            // Save tokens
            localStorage.setItem("access_token", data.tokens.access);
            localStorage.setItem("refresh_token", data.tokens.refresh);

            // Optional: Save user info
            localStorage.setItem("username", data.user.username);

            // Redirect to dashboard
            window.location.href = "/dashboard/";
        } else {
            document.getElementById("error").innerText = data.error || "Login failed";
        }
    } catch (err) {
        document.getElementById("error").innerText = "Network error: " + err.message;
    }
});
