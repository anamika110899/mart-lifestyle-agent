const API_BASE = "http://127.0.0.1:8000";

function appendMessage(role, meta, text) {
  const messagesEl = document.getElementById("messages");
  const div = document.createElement("div");
  div.className = `msg ${role}`;
  div.innerHTML = `<div class="meta">${meta}</div>${text}`;
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

async function sendMessage(text) {
  const inputEl = document.getElementById("input");
  const sendBtn = document.getElementById("sendBtn");

  if (!text) return;

  appendMessage("user", "you", text);
  inputEl.value = "";
  sendBtn.disabled = true;
  sendBtn.textContent = "Thinking…";

  try {
    const res = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });

    if (!res.ok) {
      appendMessage("bot", "error", "Backend error: " + res.status);
      return;
    }

    const data = await res.json();
    appendMessage("bot", data.agent, data.reply);

  } catch (err) {
    appendMessage("bot", "error", "Could not reach backend. Is FastAPI running?");
  }

  sendBtn.disabled = false;
  sendBtn.textContent = "Send";
}

function handleSubmit(event) {
  event.preventDefault();     //   🔥 prevents GET /chat
  const inputEl = document.getElementById("input");
  const text = inputEl.value.trim();
  if (!text) return;
  sendMessage(text);
}

function sendQuick(text) {
  sendMessage(text);
}
