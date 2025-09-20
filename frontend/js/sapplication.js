
async function fetchApplications() {
  try {
    const token = localStorage.getItem("token") || "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqYWliYWJ1QGdtYWlsLmNvbSIsInJvbGUiOiJzdHVkZW50IiwiZXhwIjoxNzU4MzczMjIxfQ.T3e_HakZLRCDvkhOQSmOIiVM3uSiFfvPBJ_edR9BDGE";
    const response = await fetch("http://localhost:8000/api/students/applications/", {
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    });

    if (!response.ok) throw new Error("Failed to fetch applications");
    const applications = await response.json();
    renderApplications(applications);
  } catch (error) {
    console.error(error);
    document.getElementById("internship-list").innerHTML =
      `<p style="color:red; text-align:center;">Unable to load applications. Please try again.</p>`;
  }
}

// Render the applications
function renderApplications(applications) {
  const container = document.getElementById("internship-list");
  container.innerHTML = "";

  applications.forEach(app => {
    const card = document.createElement("div");
    card.className = "internship-card";

    card.innerHTML = `
      <span class="status-badge status-applied">Applied</span>
      <p><strong>Application ID:</strong> ${app.id}</p>
      <p><strong>Student ID:</strong> ${app.student_id}</p>
      <p><strong>Internship ID:</strong> ${app.internship_id}</p>
      <p><strong>Cover Letter:</strong> ${app.cover_letter || "N/A"}</p>
      <p><strong>Status:</strong> ${app.status}</p>
      <p><strong>Applied At:</strong> ${new Date(app.applied_at).toLocaleString()}</p>
    `;

    container.appendChild(card);
  });
}

document.addEventListener("DOMContentLoaded", fetchApplications);
