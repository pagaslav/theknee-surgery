/* jshint esversion: 11 */
/* global $ */

/**
 * Function to handle document ready event
 */
$(document).ready(function () {
  // Get user role value
  const userRole = $("#userRole").val();
  // Check if viewing as admin
  const viewingAsAdmin = $("#viewingAsAdmin").val() === "true";
  console.log("User Role: ", userRole);
  console.log("Viewing as Admin: ", viewingAsAdmin);

  // Log error if user role is not defined
  if (!userRole) {
    console.error("User role is not defined!");
  }

  /**
   * Function to validate password on input event
   */
  $("#floatingPassword").on("input", function () {
    validatePassword($(this).val());
  });

  /**
   * Function to show or hide the back-to-top button based on scroll position
   */
  $(window).scroll(function () {
    if ($(this).scrollTop() > 100) {
      $("#back-to-top").fadeIn();
    } else {
      $("#back-to-top").fadeOut();
    }
  });

  /**
   * Function to animate scroll to top when back-to-top button is clicked
   */
  $("#back-to-top").click(function (e) {
    e.preventDefault();
    $("html, body").animate({ scrollTop: 0 }, "300");
  });

  /**
   * Function to update time and date every second
   */
  function updateTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    const options = { year: "numeric", month: "long", day: "numeric" };
    const dateString = now.toLocaleDateString("en-GB", options);
    $("#clock").text(timeString);
    $("#date").text(dateString);
  }

  // Initial call to update time
  updateTime();

  // Update time every second
  setInterval(updateTime, 1000);

  /**
   * Function to handle input changes in the '#floatingPhone' field
   */
  $("#floatingPhone").on("input", function () {
    // Check if input value length is greater than zero
    if ($(this).val().length > 0) {
      // Hide the sample text by setting opacity to 0
      $(".sample-text").css("opacity", 0);
    } else {
      // Show the sample text by setting opacity to 1
      $(".sample-text").css("opacity", 1);
    }
  });

  /**
   * Function to enable editing of user information
   */
  $("#editButton").click(function () {
    console.log("Edit button clicked");
    $('span[id$="Text"]').addClass("d-none");
    $('input[id$="Input"], div[id$="InputContainer"]').removeClass("d-none");
    $("#currentPasswordDiv").removeClass("d-none");
    $(this).addClass("d-none");
    $("#saveButton, #cancelButton").removeClass("d-none");

    // If the user is admin, enable the save button immediately
    if (userRole === "admin") {
      console.log("Admin detected, enabling save button");
      $("#saveButton").removeAttr("disabled");
    } else {
      console.log("Not an admin, userRole:", userRole);
    }
  });

  /**
   * Function to cancel editing of user information
   */
  $("#cancelButton").click(function () {
    $('span[id$="Text"]').removeClass("d-none");
    $('input[id$="Input"], div[id$="InputContainer"]').addClass("d-none");
    $("#currentPasswordDiv").addClass("d-none");
    $("#editButton").removeClass("d-none");
    $("#saveButton, #cancelButton").addClass("d-none");
  });

  /**
   * Function to enable save button only if current password is entered
   */
  $("#currentPasswordInput").on("input", function () {
    if ($(this).val().length > 0) {
      $("#saveButton").removeAttr("disabled");
    } else {
      $("#saveButton").attr("disabled", "disabled");
    }
  });

  /**
   * Function to save edited user data
   */
  $("#saveButton").click(function (e) {
    e.preventDefault();
    let formData = {
      user_id: $("#editUserIdInput").val(),
      name: $("#nameInput").val(),
      gender: $("#genderInput").val(),
      dob: $("#dobInput").val(),
      phone: $("#phoneInput").val(),
      email: $("#emailInput").val(),
      current_password: $("#currentPasswordInput").val(),
    };

    $.ajax({
      type: "POST",
      url: "/edit_user_ajax",
      contentType: "application/json",
      data: JSON.stringify(formData),
      success: function (response) {
        if (response.success) {
          alert(response.message);
          window.location.href = response.redirect; // Updated to redirect after successful email change
        } else {
          alert(response.message);
        }
      },
      error: function (xhr, status, error) {
        console.error("AJAX Error: ", status, error);
      },
    });
  });

  /**
   * Function to handle file upload
   */
  $("#uploadButton").click(function (e) {
    e.preventDefault();

    let formData = new FormData();
    formData.append("user_id", $("#uploadUserIdInput").val());
    formData.append("file", $("#fileInput")[0].files[0]);
    formData.append("file_type", $("#fileType").val());

    $.ajax({
      type: "POST",
      url: "/upload_file_ajax",
      data: formData,
      contentType: false,
      processData: false,
      success: function (response) {
        if (response.success) {
          alert(response.message);
          // Add the new file to the list without reloading
          let newFileHtml = `
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <a href="${response.file_url}" target="_blank">${response.file_name}</a>
                  <form action="/delete_file" method="post" style="display:inline;" class="delete-file-form">
                      <input type="hidden" name="file_id" value="${response.file_id}">
                      <button type="submit" class="btn btn-danger btn-sm">Delete</button>
                  </form>
                </li>`;
          $("#uploaded-files-list").append(newFileHtml);
          $("#no-files-message").hide();
        } else {
          alert(response.message);
        }
      },
      error: function (xhr, status, error) {
        console.error("AJAX Error: ", status, error);
      },
    });
  });

  /**
   * Function to confirm file deletion
   */
  $(document).on("submit", ".delete-file-form", function (event) {
    event.preventDefault();
    const confirmDelete = confirm("Are you sure you want to delete this file?");
    if (confirmDelete) {
      const form = $(this);
      $.ajax({
        type: "POST",
        url: form.attr("action"),
        data: form.serialize(),
        success: function (response) {
          if (response.success) {
            form.closest("li").remove();
            if ($("#uploaded-files-list").children().length === 0) {
              $("#no-files-message").show();
            }
          } else {
            alert("Failed to delete the file.");
          }
        },
        error: function (xhr, status, error) {
          console.error("AJAX Error: ", status, error);
        },
      });
    }
  });

  /**
   * Function to toggle visibility of change password form
   */
  $("#togglePasswordForm").click(function () {
    $("#changePasswordForm").toggleClass("d-none");
  });

  /**
   * Function to handle the deletion of an assigned patient.
   * This function retrieves the patient ID, confirms the deletion action,
   * sends an AJAX request to delete the patient, and updates the UI accordingly.
   */
  $(".delete-button-assigned").click(function () {
    // Get the patient ID from the closest list item
    const patientId = $(this).closest(".list-group-item").data("id");
    // Confirm the deletion action with the user
    const confirmation = confirm(
      "Are you sure you want to delete this patient?"
    );
    if (confirmation) {
      // If confirmed, send an AJAX request to delete the patient
      $.ajax({
        url: `/api/deletePatient/${patientId}`,
        type: "DELETE",
        // Handle the response from the server
        success: function (response) {
          if (response.success) {
            // Remove the patient element from the DOM if deletion is successful
            $(`[data-id="${patientId}"]`).remove();
          } else {
            // Alert the user if there was an error deleting the patient
            alert("Error deleting patient");
          }
        },
        // Log an error if the AJAX request fails
        error: function (xhr, status, error) {
          console.error("AJAX Error: ", status, error);
        },
      });
    }
  });
});

/**
 * Function to validate password requirements
 * @param {string} id - The ID of the password input field
 * @param {string} requirementsId - The ID of the password requirements container
 */
function validatePassword(id, requirementsId) {
  const password = document.getElementById(id).value;
  const requirements = document.getElementById(requirementsId);

  const length = requirements.querySelector('p[id^="length"]');
  const uppercase = requirements.querySelector('p[id^="uppercase"]');
  const number = requirements.querySelector('p[id^="number"]');

  // Check length
  if (password.length >= 8) {
    length.classList.remove("neutral");
    length.classList.add("valid");
  } else {
    length.classList.remove("valid");
    length.classList.add("neutral");
  }

  // Check for uppercase letter
  if (/[A-Z]/.test(password)) {
    uppercase.classList.remove("neutral");
    uppercase.classList.add("valid");
  } else {
    uppercase.classList.remove("valid");
    uppercase.classList.add("neutral");
  }

  // Check for number
  if (/\d/.test(password)) {
    number.classList.remove("neutral");
    number.classList.add("valid");
  } else {
    number.classList.remove("valid");
    number.classList.add("neutral");
  }
}

/**
 * Function to toggle password visibility
 * @param {string} passwordFieldId - The ID of the password input field
 * @param {string} iconId - The ID of the eye icon
 */
function togglePasswordVisibility(passwordFieldId, iconId) {
  const passwordField = document.getElementById(passwordFieldId);
  const icon = document.getElementById(iconId);
  if (passwordField.type === "password") {
    passwordField.type = "text";
    icon.classList.remove("fa-eye");
    icon.classList.add("fa-eye-slash");
  } else {
    passwordField.type = "password";
    icon.classList.remove("fa-eye-slash");
    icon.classList.add("fa-eye");
  }
}

/**
 * Function to validate confirm password
 * @param {string} passwordId - The ID of the password input field
 * @param {string} confirmPasswordId - The ID of the confirm password input field
 */
function validateConfirmPassword(passwordId, confirmPasswordId) {
  // Get the values of the password and confirm password input fields
  const password = document.getElementById(passwordId).value;
  const confirmPassword = document.getElementById(confirmPasswordId).value;

  // Check if the password and confirm password values match
  if (password !== confirmPassword) {
    // If they do not match, set a custom validity message
    document
      .getElementById(confirmPasswordId);
      .setCustomValidity("Passwords do not match");
  } else {
    // If they match, clear the custom validity messag
    document.getElementById(confirmPasswordId).setCustomValidity("");
  }
}
