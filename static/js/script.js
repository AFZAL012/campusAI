let activeCategory = "general";
let chartInstance = null;

/* ================= NAVIGATION ================= */
function navClick(id) {
  document.querySelectorAll("section").forEach(sec => {
    sec.classList.add("hidden");
  });

  document.getElementById(id).classList.remove("hidden");

  if (id === "admin") {
    loadAnalytics();
    loadChart();
  }
}

/* ================= CATEGORY SWITCH ================= */
function switchCategory(cat){
  activeCategory = cat;
  const chatBox = document.getElementById("chatBox");

  chatBox.innerHTML += `
    <div class="bot">📂 Switched to <b>${cat.toUpperCase()}</b> chat</div>
  `;

  chatBox.scrollTop = chatBox.scrollHeight;
}

/* ================= CHAT ================= */
function sendMessage(){
  const input = document.getElementById("userInput");
  const msg = input.value.trim();
  if(!msg) return;

  const chatBox = document.getElementById("chatBox");

  chatBox.innerHTML += `<div class="user">${msg}</div>`;

  fetch("/ask",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({
      message: `[${activeCategory}] ${msg}`
    })
  })
  .then(res => res.json())
  .then(data => {
    chatBox.innerHTML += `<div class="bot">${data.answer || "⚠️ No response"}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;

    // auto refresh analytics
    loadAnalytics();
    loadChart();
  })
  .catch(err => {
    chatBox.innerHTML += `<div class="bot">❌ Server error</div>`;
    console.error(err);
  });

  input.value="";
}

/* ================= SCHOLARSHIP ================= */
function getScholarship() {

  const profile = {
    course: course.value,
    year: year.value,
    category: category.value,
    income: income.value
  };

  fetch("/recommend_scholarship", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(profile)
  })
  .then(res => res.json())
  .then(data => {

    const chatBox = document.getElementById("chatBox");
    chatBox.innerHTML += `<div class="bot"><b>🎯 Scholarship Evaluation</b></div>`;

    if (!data.data || data.data.length === 0) {
      chatBox.innerHTML += `<div class="bot">❌ No scholarships found.</div>`;
    }

    data.data.forEach(s => {
      chatBox.innerHTML += `
        <div class="bot">
          🎓 <b>${s.name}</b><br>
          ${s.eligible ? "✅ Eligible" : "❌ Not Eligible"}<br>
          💰 ${s.benefit}<br>
          📊 Chance: ${s.probability}<br>
          ${s.reasons.join("<br>")}
        </div>
      `;
    });

    chatBox.scrollTop = chatBox.scrollHeight;

    // refresh analytics after scholarship
    loadAnalytics();
    loadChart();
  })
  .catch(err => {
    console.error(err);
  });
}

/* ================= ANALYTICS ================= */
function loadAnalytics() {
  fetch("/analytics")
    .then(res => res.json())
    .then(data => {

      // safety fallback
      totalQueries.innerText = data.total_queries ?? 0;
      examCount.innerText = data.exam ?? 0;
      scholarshipCount.innerText = data.scholarship ?? 0;

    })
    .catch(err => console.error("Analytics error:", err));
}

function loadChart() {
  fetch("/analytics")
    .then(res => res.json())
    .then(data => {

      const ctx = document.getElementById("analyticsChart");
      if (!ctx) return;

      const values = [
        data.exam ?? 0,
        data.scholarship ?? 0,
        data.library ?? 0,
        data.notice ?? 0
      ];

      if(chartInstance) chartInstance.destroy();

      chartInstance = new Chart(ctx, {
        type: "bar",
        data: {
          labels: ["Exam", "Scholarship", "Library", "Notice"],
          datasets: [{
            label: "User Queries",
            data: values,
            backgroundColor: "#22d3ee",
            borderRadius: 8
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              ticks: { color: "#fff" }
            },
            x: {
              ticks: { color: "#fff" }
            }
          },
          plugins: {
            legend: {
              labels: { color: "#fff" }
            }
          }
        }
      });

    })
    .catch(err => console.error("Chart error:", err));
}

/* ================= PARTICLES ================= */
function createParticles() {
  const container = document.getElementById("particles");
  if (!container) return;

  for (let i = 0; i < 80; i++) {
    const p = document.createElement("span");
    p.style.left = Math.random() * 100 + "vw";
    p.style.animationDuration = 6 + Math.random() * 12 + "s";
    container.appendChild(p);
  }
}

createParticles();
