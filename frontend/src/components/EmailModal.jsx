import { useState } from "react";
import "../styles/modal.css";

export default function EmailModal({ open, onClose, ticketUrl }) {
  const [email, setEmail] = useState("");
  const [optIn, setOptIn] = useState(false);

  if (!open) return null;

  const submit = (e) => {
    e.preventDefault();

    if (!email || !optIn) {
      alert("Please enter email and accept consent");
      return;
    }

    // OPTIONAL: send email to backend
    /*
    fetch("http://localhost:8000/collect-email", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email }),
    });
    */

    window.location.href = ticketUrl;
  };

  return (
    <div className="modal-backdrop">
      <div className="modal">
        <h2>Get Tickets</h2>
        <p>Enter your email to continue</p>

        <form onSubmit={submit}>
          <input
            type="email"
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <label className="optin">
            <input
              type="checkbox"
              checked={optIn}
              onChange={(e) => setOptIn(e.target.checked)}
            />
            I agree to receive event updates
          </label>

          <div className="modal-actions">
            <button type="submit" className="ticket-btn">
              CONTINUE
            </button>
            <button type="button" onClick={onClose} className="cancel">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
