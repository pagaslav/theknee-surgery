$(document).ready(function () {
  const userRole = $("#userRole").val()
  const viewingAsAdmin = $("#viewingAsAdmin").val() === "true"
  console.log("User Role: ", userRole)
  console.log("Viewing as Admin: ", viewingAsAdmin)

  if (!userRole) {
    console.error("User role is not defined!")
  }

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

  // Monitor input changes in the '#floatingPhone' field
  $("#floatingPhone").on("input", function () {
    // Check if input value length is greater than zero
    if ($(this).val().length > 0) {
      // Hide the sample text by setting opacity to 0
      $(".sample-text").css("opacity", 0)
    } else {
      // Show the sample text by setting opacity to 1
      $(".sample-text").css("opacity", 1)
    }
  })

  // Enable editing
  $("#editButton").click(function () {
    console.log("Edit button clicked")
    $('span[id$="Text"]').addClass("d-none")
    $('input[id$="Input"], div[id$="InputContainer"]').removeClass("d-none")
    $("#currentPasswordDiv").removeClass("d-none")
    $(this).addClass("d-none")
    $("#saveButton, #cancelButton").removeClass("d-none")

    // If the user is admin, enable the save button immediately
    if (userRole === "admin") {
      console.log("Admin detected, enabling save button")
      $("#saveButton").removeAttr("disabled")
    } else {
      console.log("Not an admin, userRole:", userRole)
    }
  })

  // Cancel editing
  $("#cancelButton").click(function () {
    $('span[id$="Text"]').removeClass("d-none")
    $('input[id$="Input"], div[id$="InputContainer"]').addClass("d-none")
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
      user_id: $("#editUserIdInput").val(),
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
          window.location.href = response.redirect // Updated to redirect after successful email change
        } else {
          alert(response.message)
        }
      },
      error: function (xhr, status, error) {
        console.error("AJAX Error: ", status, error)
      },
    })
  })

  // Handle file upload
  $("#uploadButton").click(function (e) {
    e.preventDefault()

    let formData = new FormData()
    formData.append("user_id", $("#uploadUserIdInput").val())
    formData.append("file", $("#fileInput")[0].files[0])
    formData.append("file_type", $("#fileType").val())

    $.ajax({
      type: "POST",
      url: "/upload_file_ajax",
      data: formData,
      contentType: false,
      processData: false,
      success: function (response) {
        if (response.success) {
          alert(response.message)
          // Add the new file to the list without reloading
          let newFileHtml = `
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <a href="${response.file_url}" target="_blank">${response.file_name}</a>
                  <form action="/delete_file" method="post" style="display:inline;" class="delete-file-form">
                      <input type="hidden" name="file_id" value="${response.file_id}">
                      <button type="submit" class="btn btn-danger btn-sm">Delete</button>
                  </form>
                </li>`
          $("#uploaded-files-list").append(newFileHtml)
          $("#no-files-message").hide()
        } else {
          alert(response.message)
        }
      },
      error: function (xhr, status, error) {
        console.error("AJAX Error: ", status, error)
      },
    })
  })

  // Confirm delete
  $(document).on("submit", ".delete-file-form", function (event) {
    event.preventDefault()
    const confirmDelete = confirm("Are you sure you want to delete this file?")
    if (confirmDelete) {
      const form = $(this)
      $.ajax({
        type: "POST",
        url: form.attr("action"),
        data: form.serialize(),
        success: function (response) {
          if (response.success) {
            form.closest("li").remove()
            if ($("#uploaded-files-list").children().length === 0) {
              $("#no-files-message").show()
            }
          } else {
            alert("Failed to delete the file.")
          }
        },
        error: function (xhr, status, error) {
          console.error("AJAX Error: ", status, error)
        },
      })
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
