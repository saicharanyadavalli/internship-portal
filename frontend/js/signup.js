document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("signupForm");
  const msgBox = document.getElementById("msg");

  if (!form) return;

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    msgBox.textContent = ""; // clear previous message

    const email = document.getElementById("username")?.value.trim() || "";
    const password = document.getElementById("password")?.value.trim() || "";
    const role = document.getElementById("role")?.value || "";
    const recaptchaResponse = grecaptcha.getResponse();

    if (!email || !password || !role) {
      msgBox.textContent = "⚠️ Please fill in all fields.";
      return;
    }

    if (!recaptchaResponse) {
      msgBox.textContent = "⚠️ Please complete the reCAPTCHA.";
      return;
    }

    const payload = { email, password, role, recaptcha: recaptchaResponse };

    try {
      const res = await fetch("http://127.0.0.1:8000/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json().catch(() => null);

      if (res.ok) {
        // store JWT token if returned
        if (data?.access_token) {
          localStorage.setItem("token", data.access_token);
        }
        msgBox.style.color = "green";
        msgBox.textContent = "🎉 Signup successful! Redirecting...";
        setTimeout(() => {
          window.location.href = "login.html";
        }, 1500);
      } else {
        // FastAPI HTTPException usually returns {detail: "..."}
        const errorMsg =
          (data && (data.detail || data.message)) ||
          `Unexpected error (status ${res.status})`;
        msgBox.style.color = "var(--danger)";
        msgBox.textContent = `❌ ${errorMsg}`;
      }
    } catch (err) {
      console.error(err);
      msgBox.style.color = "var(--danger)";
      msgBox.textContent = "⚠️ Failed to connect to server.";
    }
  });
});
