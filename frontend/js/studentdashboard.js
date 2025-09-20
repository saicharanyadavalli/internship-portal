document.addEventListener("DOMContentLoaded", function () {
    const myApplications = document.querySelector(".card:nth-child(1) a");
    const findInternships = document.querySelector(".card:nth-child(2) a");
    const careerResources = document.querySelector(".card:nth-child(3) a");
    const usernameSpan = document.querySelector("main h2 span");

    myApplications.addEventListener("click", function (e) {
      e.preventDefault();
      window.location.href = "sapplication.html"; 
    });

    findInternships.addEventListener("click", function (e) {
      e.preventDefault();
      window.location.href = "internships.html"; 
    });

    careerResources.addEventListener("click", function (e) {
      e.preventDefault();
      window.location.href = "connect.html";
    });

    // Populate [Username] from backend
    (async () => {
      try {
        const token = localStorage.getItem("token")||"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqYWliYWJ1QGdtYWlsLmNvbSIsInJvbGUiOiJzdHVkZW50IiwiZXhwIjoxNzU4MzczMjIxfQ.T3e_HakZLRCDvkhOQSmOIiVM3uSiFfvPBJ_edR9BDGE";
        if (!token) return;
        const res = await fetch("http://localhost:8000/api/students/me", {
          headers: { "Authorization": `Bearer ${token}` }
        });
        if (!res.ok) return;
        const me = await res.json();
        if (usernameSpan && (me.first_name || me.last_name)) {
          const name = [me.first_name, me.last_name].filter(Boolean).join(" ") || "Student";
          usernameSpan.textContent = name;
        }
      } catch (_) {}
    })();
  });
  
