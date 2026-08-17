// =====================================================================
// Employee Leave Management System - Client-side JavaScript
// =====================================================================

document.addEventListener("DOMContentLoaded", function () {
  initFlashAutoHide();
  initMobileNavToggle();
  initCancelConfirmation();
  initRejectConfirmation();
  initPasswordMatchCheck();
  initLeaveDateValidation();
});

// ---------------------------------------------------------------------
// Auto-hide flash messages after a few seconds
// ---------------------------------------------------------------------
function initFlashAutoHide() {
  const flashes = document.querySelectorAll(".flash");
  flashes.forEach(function (flash, index) {
    setTimeout(function () {
      flash.style.transition = "opacity 0.4s ease, transform 0.4s ease";
      flash.style.opacity = "0";
      flash.style.transform = "translateY(-8px)";
      setTimeout(function () {
        flash.remove();
      }, 400);
    }, 4000 + index * 300);
  });
}

// ---------------------------------------------------------------------
// Mobile sidebar toggle
// ---------------------------------------------------------------------
function initMobileNavToggle() {
  const toggleBtn = document.getElementById("navToggle");
  const sidebar = document.getElementById("sidebar");
  if (!toggleBtn || !sidebar) return;

  toggleBtn.addEventListener("click", function () {
    sidebar.classList.toggle("open");
  });

  document.addEventListener("click", function (event) {
    const isClickInside = sidebar.contains(event.target) || toggleBtn.contains(event.target);
    if (!isClickInside && sidebar.classList.contains("open")) {
      sidebar.classList.remove("open");
    }
  });
}

// ---------------------------------------------------------------------
// Confirm before cancelling a leave request
// ---------------------------------------------------------------------
function initCancelConfirmation() {
  const cancelForms = document.querySelectorAll(".cancel-leave-form");
  cancelForms.forEach(function (form) {
    form.addEventListener("submit", function (event) {
      const confirmed = confirm("Are you sure you want to cancel this leave request?");
      if (!confirmed) {
        event.preventDefault();
      }
    });
  });
}

// ---------------------------------------------------------------------
// Confirm before rejecting a leave request (admin)
// ---------------------------------------------------------------------
function initRejectConfirmation() {
  const rejectForms = document.querySelectorAll(".reject-leave-form");
  rejectForms.forEach(function (form) {
    form.addEventListener("submit", function (event) {
      const commentInput = form.querySelector('input[name="admin_comment"]');
      if (commentInput && commentInput.value.trim() === "") {
        alert("Please provide a reason for rejecting this leave request.");
        event.preventDefault();
        return;
      }
      const confirmed = confirm("Are you sure you want to reject this leave request?");
      if (!confirmed) {
        event.preventDefault();
      }
    });
  });
}

// ---------------------------------------------------------------------
// Password / Confirm Password live match feedback (registration form)
// ---------------------------------------------------------------------
function initPasswordMatchCheck() {
  const password = document.getElementById("password");
  const confirmPassword = document.getElementById("confirm_password");
  const feedback = document.getElementById("passwordMatchFeedback");

  if (!password || !confirmPassword || !feedback) return;

  function checkMatch() {
    if (confirmPassword.value === "") {
      feedback.textContent = "";
      return;
    }
    if (password.value === confirmPassword.value) {
      feedback.textContent = "Passwords match.";
      feedback.style.color = "#16a34a";
    } else {
      feedback.textContent = "Passwords do not match.";
      feedback.style.color = "#dc2626";
    }
  }

  password.addEventListener("input", checkMatch);
  confirmPassword.addEventListener("input", checkMatch);
}

// ---------------------------------------------------------------------
// Basic client-side date validation on the Apply Leave form
// ---------------------------------------------------------------------
function initLeaveDateValidation() {
  const form = document.getElementById("applyLeaveForm");
  if (!form) return;

  const startDate = document.getElementById("start_date");
  const endDate = document.getElementById("end_date");

  const today = new Date().toISOString().split("T")[0];
  if (startDate) startDate.setAttribute("min", today);

  function syncEndMin() {
    if (startDate && startDate.value) {
      endDate.setAttribute("min", startDate.value);
    }
  }

  if (startDate && endDate) {
    startDate.addEventListener("change", syncEndMin);
  }

  form.addEventListener("submit", function (event) {
    if (!startDate.value || !endDate.value) {
      return; // let backend/HTML5 required handle it
    }
    if (new Date(endDate.value) < new Date(startDate.value)) {
      alert("End date cannot be before start date.");
      event.preventDefault();
    }
    if (new Date(startDate.value) < new Date(today)) {
      alert("Start date cannot be before the current date.");
      event.preventDefault();
    }
  });
}
