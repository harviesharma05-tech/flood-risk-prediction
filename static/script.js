// Small UX helper: prevent double submission and show a submitting state.
document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form.form-grid");
  if (!form) return;

  form.addEventListener("submit", () => {
    const btn = form.querySelector(".submit-btn");
    if (btn) {
      btn.textContent = "Predicting…";
      btn.disabled = true;
    }
  });
});
