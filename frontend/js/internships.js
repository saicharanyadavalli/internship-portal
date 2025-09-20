// ✅ Note token at the start
const token = localStorage.getItem("token")||"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqYWliYWJ1QGdtYWlsLmNvbSIsInJvbGUiOiJzdHVkZW50IiwiZXhwIjoxNzU4MzY2MjQ3fQ.GqXRbdE3KyUMhF_Qzwv0imqg-Mig75w20JkFchgc5pk";

// Fetch internships from real API
async function fetchInternships() {
  try {
    const response = await fetch("http://localhost:8000/api/companies/fetchinternships", {
      headers: {
        "Authorization": "Bearer " + (token ||
          "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqYWliYWJ1QGdtYWlsLmNvbSIsInJvbGUiOiJzdHVkZW50IiwiZXhwIjoxNzU4MzY2MjQ3fQ.GqXRbdE3KyUMhF_Qzwv0imqg-Mig75w20JkFchgc5pk"),
        "Content-Type": "application/json"
      }
    });

    if (!response.ok) {
      throw new Error("Failed to fetch internships");
    }

    const internships = await response.json();
    renderInternships(internships);
  } catch (error) {
    console.error("Error:", error);
    document.getElementById("internship-list").innerHTML =
      `<p style="color:red; text-align:center;">Unable to load internships. Please try again.</p>`;
  }
}

// Render internships into cards
function renderInternships(internships) {
  const container = document.getElementById("internship-list");
  container.innerHTML = "";

  internships.forEach(internship => {
    const card = document.createElement("div");
    card.className = "internship-card";

    const isOpen = internship.deadline && new Date(internship.deadline) >= new Date();

    card.innerHTML = `
      <span class="status-badge ${isOpen ? "status-open" : "status-closed"}">
        ${isOpen ? "Open" : "Closed"}
      </span>
      <img src="${internship.company.logo_url}" alt="${internship.company.name}" class="company-logo">
      <div class="internship-details">
        <h2>${internship.title}</h2>
        <p><strong>Company:</strong> ${internship.company.name}</p>
        <p><strong>Description:</strong> ${internship.description}</p>
        <p class="requirements"><strong>Requirements:</strong> ${internship.requirements}</p>
        <p><strong>Stipend:</strong> ${internship.stipend}</p>
        <p><strong>Duration:</strong> ${internship.duration}</p>
        <p><strong>Location:</strong> ${internship.location}</p>
        <p class="deadline"><strong>Deadline:</strong> ${internship.deadline ? new Date(internship.deadline).toLocaleDateString() : "N/A"}</p>
        <button class="apply-btn" onclick="window.open('${internship.company.website}', '_blank')">Visit official site</button>
        ${isOpen ? `<button class="apply-btn apply-now" data-id="${internship.id}">Apply Now</button>` : ""}

        ${isOpen ? `
        <div class="apply-panel hidden">
          <label for="cover-${internship.id}" class="cover-label">Cover Letter (optional)</label>
          <textarea id="cover-${internship.id}" class="cover-input" rows="4" placeholder="Write your cover letter here..."></textarea>
          <div class="apply-actions">
            <button class="apply-btn confirm-apply" data-id="${internship.id}">Confirm Apply</button>
            <button class="apply-btn cancel-apply">Cancel</button>
          </div>
        </div>
        ` : ""}
      </div>
    `;

    container.appendChild(card);

    if (isOpen) {
      const applyBtn = card.querySelector('.apply-now');
      const panel = card.querySelector('.apply-panel');
      const confirmBtn = card.querySelector('.confirm-apply');
      const cancelBtn = card.querySelector('.cancel-apply');
      const coverInput = card.querySelector('.cover-input');

      if (applyBtn && panel && confirmBtn && cancelBtn && coverInput) {
        applyBtn.addEventListener('click', (e) => {
          e.preventDefault();
          panel.classList.toggle('hidden');
          if (!panel.classList.contains('hidden')) {
            coverInput.focus();
          }
        });

        cancelBtn.addEventListener('click', (e) => {
          e.preventDefault();
          panel.classList.add('hidden');
        });

        confirmBtn.addEventListener('click', async (e) => {
          e.preventDefault();
          confirmBtn.disabled = true;
          applyBtn.disabled = true;
          try {
            const internshipId = Number(confirmBtn.getAttribute('data-id'));
            const cover = (coverInput.value || '').trim() || null;
            await applyToInternship(internshipId, cover);
            applyBtn.textContent = 'Applied';
            applyBtn.classList.add('applied');
            panel.classList.add('hidden');
          } catch (err) {
            console.error('Apply failed', err);
            alert('Failed to apply. Please try again.');
            applyBtn.disabled = false;
          } finally {
            confirmBtn.disabled = false;
          }
        });
      }
    }
  });
}

// Run on page load
document.addEventListener("DOMContentLoaded", fetchInternships);

// Apply to internship
async function applyToInternship(internshipId, coverLetter) {
  if (!token) {
    alert("Please login to apply.");
    throw new Error("Token not found in localStorage");
  }

  const response = await fetch("http://localhost:8000/api/students/applications", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify({
      internship_id: Number(internshipId),
      cover_letter: (coverLetter || "").trim() || null
    })
  });

  if (!response.ok) {
    const msg = await response.text().catch(() => "");
    throw new Error(msg || "Failed to apply");
  }
  return response.json();
}
