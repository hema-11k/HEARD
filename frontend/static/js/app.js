// HEARD frontend interactions
const API_BASE = "http://127.0.0.1:8000";

function safeReadSession(key, fallback) {
  try {
    return JSON.parse(sessionStorage.getItem(key) || JSON.stringify(fallback));
  } catch (_) {
    return fallback;
  }
}

// Chat page: send the user's message to the backend assessment endpoint.
const chatForm = document.getElementById("chatForm");
if (chatForm) {
  const messages = document.getElementById("messages");
  const input = document.getElementById("chatInput");

  function addMessage(text, who) {
    const row = document.createElement("div");
    row.className = "message " + who;
    const avatar = document.createElement("span");
    avatar.className = who === "assistant" ? "mini-avatar" : "user-avatar";
    avatar.textContent = who === "assistant" ? "♥" : "You";
    const bubble = document.createElement("div");
    bubble.className = "bubble";
    const p = document.createElement("p");
    p.textContent = text;
    bubble.appendChild(p);
    row.append(avatar, bubble);
    messages.appendChild(row);
    messages.scrollTop = messages.scrollHeight;
  }

  chatForm.addEventListener("submit", async function (event) {
    event.preventDefault();
    const text = input.value.trim();
    if (!text) return;
    addMessage(text, "user");
    input.value = "";

    const waiting = "Checking your information…";
    addMessage(waiting, "assistant");
    const waitingMessage = messages.lastElementChild?.querySelector("p");

    try {
      const response = await fetch(API_BASE + "/assess", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
      });
      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.detail?.message || payload.detail?.reason || "Assessment failed.");
      }
      const analysis = payload.analysis;
      if (!analysis) throw new Error("The backend response did not include an analysis.");

      sessionStorage.setItem("heardAnalysis", JSON.stringify(analysis));
      if (waitingMessage) {
        const parts = [analysis.disclaimer || ""];
        if (analysis.red_flag && analysis.red_flags?.length) {
          parts.push("Important safety flags: " + analysis.red_flags.join(", "));
        }
        if (analysis.safety_guidance) parts.push("Safety guidance: " + analysis.safety_guidance);
        (analysis.findings || []).forEach(item => parts.push(item.text || String(item)));
        if (analysis.questions_for_doctor?.length) {
          parts.push("Questions for your doctor:\n- " + analysis.questions_for_doctor.join("\n- "));
        }
        waitingMessage.textContent = parts.filter(Boolean).join("\n\n") || "Assessment received.";
      }
    } catch (error) {
      if (waitingMessage) waitingMessage.textContent = "Could not complete the assessment: " + error.message;
    }
  });

  document.querySelectorAll("[data-prompt]").forEach(button => {
    button.addEventListener("click", function () {
      input.value = button.dataset.prompt;
      input.focus();
    });
  });
}

// Summary page edit toggle.
const editButton = document.getElementById("editSummary");
const editArea = document.getElementById("editArea");
if (editButton && editArea) {
  editButton.addEventListener("click", () => editArea.classList.toggle("hidden"));
}

// Symptoms intake wizard.
const intake = document.getElementById("appointmentForm");
if (intake) {
  let step = 1;
  const pages = Array.from(document.querySelectorAll(".form-step"));
  const prev = document.getElementById("prevStep");
  const next = document.getElementById("nextStep");
  const finish = document.getElementById("finishStep");

  function escapeHTML(value) {
    return String(value).replace(/[&<>"']/g, character => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
    })[character]);
  }

  function render() {
    pages.forEach(page => page.classList.toggle("active", Number(page.dataset.step) === step));
    document.querySelectorAll("[data-step-label]").forEach(label => {
      label.classList.toggle("current", Number(label.dataset.stepLabel) === step);
    });
    if (prev) prev.disabled = step === 1;
    if (next) next.classList.toggle("hidden", step === 3);
    if (finish) {
      finish.classList.toggle("hidden", step !== 3);
      if (!finish.disabled) finish.textContent = "View summary →";
    }

    const stepCount = document.getElementById("stepCount");
    const stepProgress = document.getElementById("stepProgress");
    if (stepCount) stepCount.textContent = step + " / 3";
    if (stepProgress) stepProgress.textContent = "Step " + step + " of 3";

    if (step === 3) {
      const data = new FormData(intake);
      const fields = [
        ["Main concern", data.get("concern") || "Not specified"],
        ["Description", data.get("description") || "Not added"],
        ["Duration", data.get("duration") || "Not specified"],
        ["Cycle pattern", data.get("cycle") || "Not specified"],
        ["Last period", data.get("lastPeriod") || "Not added"],
        ["Planned test", data.get("plannedTest") || "None"],
        ["Pain", data.get("pain") || "Not specified"],
        ["Other notes", data.get("medicines") || "Not added"]
      ];
      const reviewList = document.getElementById("reviewList");
      if (reviewList) {
        reviewList.innerHTML = fields.map(([key, value]) =>
          '<div class="review-row"><span>' + escapeHTML(key) +
          '</span><b>' + escapeHTML(value) + '</b></div>'
        ).join("");
      }
    }
  }

  if (next) next.addEventListener("click", () => {
    if (step < 3) { step++; render(); }
  });
  if (prev) prev.addEventListener("click", () => {
    if (step > 1) { step--; render(); }
  });

  if (finish) {
    finish.addEventListener("click", async function () {
      if (finish.disabled) return;
      const data = {};
      new FormData(intake).forEach((value, key) => { data[key] = value; });

      // Convert the whole form into clear text for the backend parser.
      const text = [
        "Main concern: " + (data.concern || "not specified"),
        "Description: " + (data.description || "not provided"),
        "Duration: " + (data.duration || "not specified"),
        "Cycle pattern: " + (data.cycle || "not specified"),
        "Last period: " + (data.lastPeriod || "not provided"),
        "Planned test: " + (data.plannedTest || "none"),
        "Pain: " + (data.pain || "not specified"),
        "Medicines and notes: " + (data.medicines || "not provided"),
        "Questions for clinician: " + (data.questions || "none added")
      ].join("\n");

      finish.disabled = true;
      finish.textContent = "Analyzing…";
      let timeoutId;
      const controller = new AbortController();
      timeoutId = setTimeout(() => controller.abort(), 120000);

      try {
        const response = await fetch(API_BASE + "/assess", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text }),
          signal: controller.signal
        });

        let payload;
        try {
          payload = await response.json();
        } catch (_) {
          throw new Error("Backend returned an unreadable response. Check the backend terminal.");
        }

        if (!response.ok) {
          const detail = payload.detail;
          throw new Error(
            (typeof detail === "string" ? detail : detail?.message || detail?.reason) ||
            ("Backend returned HTTP " + response.status)
          );
        }
        if (!payload.analysis) {
          throw new Error("Backend responded, but the analysis field is missing.");
        }

        sessionStorage.setItem("heardDemoAnswers", JSON.stringify(data));
        sessionStorage.setItem("heardAnalysis", JSON.stringify(payload.analysis));
        window.location.assign("/summary.html");
      } catch (error) {
        const message = error.name === "AbortError"
          ? "Analysis took more than 2 minutes. Check the backend terminal and try again."
          : error.message || "Unexpected error while analyzing.";
        alert(message);
        finish.disabled = false;
        finish.textContent = "Try again";
      } finally {
        clearTimeout(timeoutId);
      }
    });
  }
  render();
}