$(document).ready(function () {
  $("#floatingPassword").on("input", function () {
    let password = $(this).val()

    // Check the length of the password
    if (password.length >= 8) {
      $("#length").removeClass("neutral invalid").addClass("valid")
    } else {
      $("#length").removeClass("neutral valid").addClass("invalid")
    }

    // Check for uppercase letter
    if (/[A-Z]/.test(password)) {
      $("#uppercase").removeClass("neutral invalid").addClass("valid")
    } else {
      $("#uppercase").removeClass("neutral valid").addClass("invalid")
    }

    // Check for number
    if (/\d/.test(password)) {
      $("#number").removeClass("neutral invalid").addClass("valid")
    } else {
      $("#number").removeClass("neutral valid").addClass("invalid")
    }
  })
})

function togglePasswordVisibility(inputId, iconId) {
  let passwordInput = document.getElementById(inputId)
  let passwordIcon = document.getElementById(iconId)
  if (passwordInput.type === "password") {
    passwordInput.type = "text"
    passwordIcon.classList.remove("fa-eye")
    passwordIcon.classList.add("fa-eye-slash")
  } else {
    passwordInput.type = "password"
    passwordIcon.classList.remove("fa-eye-slash")
    passwordIcon.classList.add("fa-eye")
  }
}
