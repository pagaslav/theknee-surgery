/* jshint esversion: 8 */

/**
 * This script is used to handle the logout confirmation modal.
 * When the user clicks the "Log Out" link, the modal will be displayed.
 * If the user confirms the logout by clicking the "Yes, log out" button,
 * the browser will navigate to the logout URL.
 */
$(document).ready(function () {
  // Attach a click event handler to the confirmLogout button
  $("#confirmLogout").click(function () {
    // Redirect the user to the logout URL
    window.location.href = "{{ url_for('logout') }}"
  })
})
