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

  // Function to update the time and date
  function updateTime() {
    const now = new Date()
    const timeString = now.toLocaleTimeString()
    const options = { year: "numeric", month: "long", day: "numeric" }
    const dateString = now.toLocaleDateString("en-GB", options)
    $("#clock").text(timeString)
    $("#date").text(dateString)
  }

  // Initial call to update time
  updateTime()

  // Update time every second
  setInterval(updateTime, 1000)
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
