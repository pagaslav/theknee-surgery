$(document).ready(function () {
  $("#floatingPassword").on("input", function () {
    validatePassword($(this).val())
  })

  // Show or hide the button
  $(window).scroll(function () {
    if ($(this).scrollTop() > 100) {
      $("#back-to-top").fadeIn()
    } else {
      $("#back-to-top").fadeOut()
    }
  })

  // Animate the scroll to top
  $("#back-to-top").click(function (e) {
    e.preventDefault()
    $("html, body").animate({ scrollTop: 0 }, "300")
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

  // Enable editing
  $("#editButton").click(function () {
    $('span[id$="Text"]').addClass("d-none")
    $('input[id$="Input"]').removeClass("d-none")
    $("#currentPasswordDiv").removeClass("d-none")
    $(this).addClass("d-none")
    $("#saveButton, #cancelButton").removeClass("d-none")
  })

  // Cancel editing
  $("#cancelButton").click(function () {
    $('span[id$="Text"]').removeClass("d-none")
    $('input[id$="Input"]').addClass("d-none")
    $("#currentPasswordDiv").addClass("d-none")
    $("#editButton").removeClass("d-none")
    $("#saveButton, #cancelButton").addClass("d-none")
  })

  // Enable save button only if current password is entered
  $("#currentPasswordInput").on("input", function () {
    if ($(this).val().length > 0) {
      $("#saveButton").removeAttr("disabled")
    } else {
      $("#saveButton").attr("disabled", "disabled")
    }
  })

  // Save edited data
  $("#saveButton").click(function (e) {
    e.preventDefault()
    let formData = {
      name: $("#nameInput").val(),
      gender: $("#genderInput").val(),
      dob: $("#dobInput").val(),
      phone: $("#phoneInput").val(),
      email: $("#emailInput").val(),
      current_password: $("#currentPasswordInput").val(),
    }

    $.ajax({
      type: "POST",
      url: "/edit_user_ajax",
      contentType: "application/json",
      data: JSON.stringify(formData),
      success: function (response) {
        if (response.success) {
          alert(response.message)
          location.reload()
        } else {
          alert(response.message)
        }
      },
      error: function (response) {
        alert(response.responseJSON.message)
      },
    })
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

function validatePassword(password) {
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
}
