# The Knee surgery README

![Responsive Mockup](static/documentation/respons-knee.webp)

View the live site [here](https://theknee-surgery-f5b49706e9d6.herokuapp.com/)

## Introduction
Welcome to The Knee Surgery Clinic, your trusted destination for expert knee care and surgery. Our website is designed to offer patients a seamless experience, from registration to recovery. As a patient, you can easily register, request appointments, and communicate with our dedicated clinic staff. Our team is here to approve your requests, assign you to the right doctor, and schedule your appointments based on your specific needs. Doctors can review patient information, set exact dates and times for consultations, and update medical records to ensure you receive the best possible care. We are committed to providing a user-friendly platform that connects you with our skilled medical professionals and supports you throughout your knee surgery journey. Join us at The Knee Surgery Clinic and take the first step towards a healthier, pain-free life.

## Project Goals
The primary goal of The Knee Surgery Clinic website is to streamline the process of knee care for both patients and medical professionals. Our objectives include:

  1.	**Simplified Patient Registration**: Enable new patients to easily register on the platform and provide essential medical information.
  2.	**Efficient Appointment Requests**: Allow patients to request appointments with our doctors, ensuring that their needs are addressed promptly.
  3.	**Seamless Communication**: Facilitate clear and effective communication between patients, clinic staff, and doctors.
  4.	**Comprehensive Medical Record Management**: Provide doctors with the tools to manage and update patient medical records efficiently.
  5.	**Optimized Scheduling**: Assist clinic staff in approving appointment requests and assigning them to the appropriate doctors, ensuring that appointments are scheduled at convenient times for both patients and doctors.
  6.	**Enhanced User Experience**: Offer a user-friendly interface that simplifies the entire process, from registration to receiving care, making it accessible to all users.
  7.	**Patient Empowerment**: Empower patients with access to their medical records and the ability to track their treatment progress, promoting a proactive approach to their health.

Our mission is to provide a platform that not only improves the efficiency of clinic operations but also enhances the overall experience for our patients, ensuring they receive the best possible knee care.

## User Stories

### First Time Visitor Goals:

1. As a first-time visitor, I want to quickly understand what **The Knee surgery** offers so I can start managing my knee health effectively.
2. As a first-time visitor, I'm looking for an easy way to register as a patient and provide my medical information without any confusion, ensuring a smooth start.
3. As a first-time visitor, I want to learn about the clinic’s doctors and their expertise, so I feel assured about the quality of care I will receive.
4. As a first-time visitor, I’m looking for contact details and the clinic’s location to easily reach out for further assistance or plan a visit.

### Returning Visitor Goals:

1. As a returning visitor, I want to easily log into my account to access my medical records and upcoming appointment details.
2. As a returning visitor, I’m looking for a quick way to request a follow-up appointment or update an existing appointment.
3. As a returning visitor, I want to review and update my personal information to ensure my profile is current and accurate.

## User Experience (UX) &

User Interface (UI)

### Wireframes

- Home Page
  ![Home Page]()
  ...
- Map of website
  ![Map of website]()

### Colour Scheme

#### Color Palette

The chosen color palette for The Knee Surgery is designed to evoke a sense of calmness and natural balance. The colors are as follows:

- **Primary Color**: `#198754` or Bootstrap bg-success (Green)
- **Secondary Color**: `#c8e6c9` (Light Green)
- **Accent Color**: `#ffffff` (White)
- **Complementary Color**: `#ffb74d` (Soft Orange)
- **Neutral Color**: `#9e9e9e` (Grey)

#### Color Psychology and Usage

- **Green (`#198754` or Bootstrap bg-success)**: This color represents health, growth, and tranquility. It is the primary color and will be used for main elements and headings to convey a sense of wellbeing and balance.
- **Light Green (`#c8e6c9`)**: Soft and calming, this color is ideal for background sections. It creates a serene and refreshing atmosphere, making the website more welcoming.
- **White (`#ffffff`)**: Symbolizing purity and simplicity, white will be used for text and borders to ensure clarity and readability.
- **Soft Orange (`#ffb74d`)**: Adding a touch of warmth and friendliness, soft orange will be used for call-to-action buttons, drawing attention without being too aggressive.
- **Grey (`#9e9e9e`)**: This neutral color provides balance and stability. It will be used for less prominent text, ensuring that primary content stands out without distraction.

![Colour Palette](static/documentation/color-palette.jpg)

#### Visual Harmony and Accessibility

- **Contrast and Readability**: Ensure there is sufficient contrast between the primary color (Green) and the accent color (White) for text and important elements to maintain readability.
- **Balance**: Use soft orange sparingly to highlight key actions without overwhelming the natural and calm aesthetic of the site.
- **Consistency**: Maintain a consistent use of colors throughout the website to create a harmonious visual experience that supports the site’s calming and professional atmosphere.
- **Accessibility**: Consider accessibility guidelines, ensuring that all text is readable by maintaining an appropriate contrast ratio and using color combinations that are friendly for users with color vision deficiencies. This includes testing the color palette with accessibility tools to verify compliance with WCAG standards.

### Typography

#### Logo Font

#### Slogan Font

#### Quote Font

#### Button and Body Text Font

#### Description Font on ... Page

### The Knee surgery Logo

## Features

### Navigation

#### Navbar

##### Desktop View:

##### Responsive Design:

##### Mobile View:

### Footer

##### Desktop View:

##### Responsive Design:

##### Mobile View:

### Home Page

#### Quote Feature:

#### Main Interactive Buttons:

### Learn Page

#### Navigation Controls:

#### Content Layout:

## Technologies Used

## Testing

### Responsiveness

### Validator testing

#### HTML

#### CSS

#### JavaScript

### LightHouse report

### Compatibility

### Bugs

#### SSL

**SSL Certificate Verification Failed When Connecting to MongoDB:** Encountered an SSL certificate verification error (SSL: CERTIFICATE_VERIFY_FAILED) when trying to connect to MongoDB.

![Bug 1, code](static/documentation/bugs/1/bug-1.jpg)
![Bug 1, Error Message](static/documentation/bugs/1/bug-1-1.jpg)

**Solution:** Resolved the issue by adding the certifi library (import certifi) and modifying the PyMongo initialization line to specify the tlsCAFile parameter.

**Code Changes and Result:**

![Bug 1, Code Changes](static/documentation/bugs/1/bug-1-2.jpg)
![Bug 1, Result](static/documentation/bugs/1/bug-1-3.jpg)

#### Logout Issue

**Problem:**
When a user clicks the "Log Out" link and confirms the logout, the user is redirected to the homepage, but the navigation menu still shows the logged-in state (i.e., it still shows "Profile" and "Log Out" instead of "Log In" and "Sign Up"). Additionally, the user can still access the profile page.
**Steps to Reproduce:**

1.  Log in to your account.
2.  Click the "Log Out" link.
3.  Confirm the logout.
    **Cause:**
    The issue was caused by the JavaScript code for the logout not being correctly executed within the context of the Flask application, leading to the user session not being properly terminated on the server side. This issue is specific to how Jinja templates are rendered and how JavaScript interacts with the Flask backend.
    Initially, the JavaScript code for the logout was included in a custom JavaScript file. This caused the problem as described because the Jinja templating was not correctly interacting with the external JavaScript file. Once the code was moved directly into the `base.html` template, everything worked as expected.
    **Solution:**
    Ensure the JavaScript code is included at the right place in the `base.html` template to properly interact with the Flask backend:

            ```html
            <!-- Inline script for logout modal -->
            <script>
              $(document).ready(function () {
                // Attach a click event handler to the confirmLogout button
                $("#confirmLogout").click(function () {
                  // Redirect the user to the logout URL
                  window.location.href = "{{ url_for('logout') }}"
                })
              })
            </script>
            ```

        After implementing the above solution, the logout functionality works as expected, with the user being properly logged out and the navigation menu updating correctly to reflect the logged-out state.

#### User Email Update Issue

**Problem:**
When a user updates their email address in the profile settings, the user remains logged in with the new email address, but they are redirected to the home page. Upon returning to the profile page, the user’s profile information is displayed correctly, but a “User not found” notification appears at the top of the page.

**Steps to Reproduce:**

    1.	Log in to your account.
    2.	Go to the profile page.
    3.	Click the “Edit” button to enable editing mode.
    4.	Change the email address to a new valid email address.
    5.	Enter the current password and click “Save.”
    6.	Observe the redirection to the home page.
    7.	Navigate back to the profile page.
    8.	Observe the “User not found” notification at the top of the page.

**Expected Behavior:**

    •	The user should remain on the profile page after updating the email address.
    •	No “User not found” notification should appear if the profile information is displayed correctly.

**Actual Behavior:**

    •	The user is redirected to the home page after updating the email address.
    •	A “User not found” notification appears at the top of the profile page upon returning.

**Screenshot:**
![Bug 3, User not found Message](static/documentation/bugs/1/bug-3-1.webp)

**Cause:**
The issue was caused by the Flask application not correctly updating the session and redirecting after an email change. Although the session email was updated, the redirection logic did not reflect the new session state, leading to the user being treated as unauthenticated or non-existent in subsequent requests.

**Solution:**
Ensure that after updating the email in the session, the user is redirected correctly and the session state is fully updated:

      ```python
      # Update session email if changed
      if current_email != new_email:
          session["user"] = new_email
          flash("Your email has been updated to {}.".format(new_email), "success")
          return {"success": True, "message": "Your email has been updated.", "redirect": url_for("profile", username=new_email)}
      else:
          flash("Your information has been updated.", "success")
          return {"success": True, "message": "Your information has been updated.", "redirect": url_for("profile", username=current_email)}

Ensure the JavaScript handles the success response correctly:

      ```javascript
      success: function (response) {
        if (response.success) {
          alert(response.message);
          window.location.href = response.redirect; // Updated to redirect after successful email change
        } else {
          alert(response.message);
        }
      }

After implementing the above solution, the email change functionality works as expected, keeping the user authenticated with the new email address and displaying the appropriate success message on the profile page.

![Bug 3, Result](static/documentation/bugs/1/bug-3-2.webp)

### Unsolved Bugs

### Mistakes

## Deployment

### Deployment to GitHub Pages

### Deployment to Heroku

### Local Deployment

## Credits

### Content

#### Terms and Conditions

The Terms and Conditions for this project were sourced from [TermsFeed](https://www.termsfeed.com/), a platform that provides templates and generators for legal documents. These terms were adapted to fit the specific needs of The Knee Surgery website, ensuring that they are relevant to the services provided and the target audience. This addition helps make the project more realistic and professional by outlining the legal guidelines and user responsibilities clearly.

#### Privacy Policy

The Privacy Policy was also generated using [TermsFeed](https://www.termsfeed.com/), ensuring comprehensive coverage of all necessary legal aspects related to user data and privacy. This policy was customized to align with the operations and data handling practices of The Knee Surgery website. Including a Privacy Policy enhances the authenticity of the project, demonstrating a commitment to user privacy and data protection, which is crucial for any real-world website.

### Images

#### Index page

1. Doctor Illustrator Design, [License.](documentation/licenses/photos/image-1-license-certificate.txt)
2. Physiotherapist check X ray, [License.](documentation/licenses/photos/image-2-license-certificate.txt)
3. Hands operating a patient, [License.](documentation/licenses/photos/image-3-license-certificate.txt)
4. Knee joint model , [License.](documentation/licenses/photos/image-4-license-certificate.txt)
5. Ligament Reconstruction image was generated using AI from [ChatGPT](https://www.openai.com/chatgpt)
6. Bandaging woman's injured knee, [License.](documentation/licenses/photos/image-6-license-certificate.txt)
7. Injection Procedures, [License.](documentation/licenses/photos/image-7-license-certificate.txt)

#### Our Doctors page

1. Dr. John Doe photo, [License.](documentation/licenses/photos/image-8-license-certificate.txt)
2. Dr. Jane Smith photo, [License.](documentation/licenses/photos/image-9-license-certificate.txt)
3. Dr. Emily Johnson photo, [License.](documentation/licenses/photos/image-10-license-certificate.txt)
4. Dr. Michael Brown photo, [License.](documentation/licenses/photos/image-11-license-certificate.txt)

#### About Us page

1. Hospital reception counter, [License.](documentation/licenses/photos/image-12-license-certificate.txt)
2. Busy Hospital Corridor, [License.](documentation/licenses/photos/image-13-license-certificate.txt)
3. Modern operating theatre, [License.](documentation/licenses/photos/image-14-license-certificate.txt)
4. A room of an hospital, [License.](documentation/licenses/photos/image-15-license-certificate.txt)

## Acknowledgments

## Future Improvements

---

![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

Welcome USER_NAME,

This is the Code Institute student template for Gitpod. We have preinstalled all of the tools you need to get started. It's perfectly ok to use this template as the basis for your project submissions.

You can safely delete this README.md file or change it for your own project. Please do read it at least once, though! It contains some important information about Gitpod and the extensions we use. Some of this information has been updated since the video content was created. The last update to this file was: **June 18, 2024**

## Gitpod Reminders

To run a frontend (HTML, CSS, Javascript only) application in Gitpod, in the terminal, type:

`python3 -m http.server`

A blue button should appear to click: _Make Public_,

Another blue button should appear to click: _Open Browser_.

To run a backend Python file, type `python3 app.py` if your Python file is named `app.py`, of course.

A blue button should appear to click: _Make Public_,

Another blue button should appear to click: _Open Browser_.

By Default, Gitpod gives you superuser security privileges. Therefore, you do not need to use the `sudo` (superuser do) command in the bash terminal in any of the lessons.

To log into the Heroku toolbelt CLI:

1. Log in to your Heroku account and go to _Account Settings_ in the menu under your avatar.
2. Scroll down to the _API Key_ and click _Reveal_
3. Copy the key
4. In Gitpod, from the terminal, run `heroku_config`
5. Paste in your API key when asked

You can now use the `heroku` CLI program - try running `heroku apps` to confirm it works. This API key is unique and private to you, so do not share it. If you accidentally make it public, you can create a new one with _Regenerate API Key_.

### Connecting your Mongo database

- **Connect to Mongo CLI on a IDE**
- navigate to your MongoDB Clusters Sandbox
- click **"Connect"** button
- select **"Connect with the MongoDB shell"**
- select **"I have the mongo shell installed"**
- choose **mongosh (2.0 or later)** for : **"Select your mongo shell version"**
- choose option: **"Run your connection string in your command line"**
- in the terminal, paste the copied code `mongo "mongodb+srv://<CLUSTER-NAME>.mongodb.net/<DBname>" --apiVersion 1 --username <USERNAME>`
  - replace all `<angle-bracket>` keys with your own data
- enter password _(will not echo **\*\*\*\*** on screen)_

---

## Release History

We continually tweak and adjust this template to help give you the best experience. Here is the version history:

**June 18, 2024,** Add Mongo back into template

**June 14, 2024,** Temporarily remove Mongo until the key issue is resolved

**May 28 2024:** Fix Mongo and Links installs

**April 26 2024:** Update node version to 16

**September 20 2023:** Update Python version to 3.9.17.

**September 1 2021:** Remove `PGHOSTADDR` environment variable.

**July 19 2021:** Remove `font_fix` script now that the terminal font issue is fixed.

**July 2 2021:** Remove extensions that are not available in Open VSX.

**June 30 2021:** Combined the P4 and P5 templates into one file, added the uptime script. See the FAQ at the end of this file.

**June 10 2021:** Added: `font_fix` script and alias to fix the Terminal font issue

**May 10 2021:** Added `heroku_config` script to allow Heroku API key to be stored as an environment variable.

**April 7 2021:** Upgraded the template for VS Code instead of Theia.

**October 21 2020:** Versions of the HTMLHint, Prettier, Bootstrap4 CDN and Auto Close extensions updated. The Python extension needs to stay the same version for now.

**October 08 2020:** Additional large Gitpod files (`core.mongo*` and `core.python*`) are now hidden in the Explorer, and have been added to the `.gitignore` by default.

**September 22 2020:** Gitpod occasionally creates large `core.Microsoft` files. These are now hidden in the Explorer. A `.gitignore` file has been created to make sure these files will not be committed, along with other common files.

**April 16 2020:** The template now automatically installs MySQL instead of relying on the Gitpod MySQL image. The message about a Python linter not being installed has been dealt with, and the set-up files are now hidden in the Gitpod file explorer.

**April 13 2020:** Added the _Prettier_ code beautifier extension instead of the code formatter built-in to Gitpod.

**February 2020:** The initialisation files now _do not_ auto-delete. They will remain in your project. You can safely ignore them. They just make sure that your workspace is configured correctly each time you open it. It will also prevent the Gitpod configuration popup from appearing.

**December 2019:** Added Eventyret's Bootstrap 4 extension. Type `!bscdn` in a HTML file to add the Bootstrap boilerplate. Check out the <a href="https://github.com/Eventyret/vscode-bcdn" target="_blank">README.md file at the official repo</a> for more options.

---

## FAQ about the uptime script

**Why have you added this script?**

It will help us to calculate how many running workspaces there are at any one time, which greatly helps us with cost and capacity planning. It will help us decide on the future direction of our cloud-based IDE strategy.

**How will this affect me?**

For everyday usage of Gitpod, it doesn’t have any effect at all. The script only captures the following data:

- An ID that is randomly generated each time the workspace is started.
- The current date and time
- The workspace status of “started” or “running”, which is sent every 5 minutes.

It is not possible for us or anyone else to trace the random ID back to an individual, and no personal data is being captured. It will not slow down the workspace or affect your work.

**So….?**

We want to tell you this so that we are being completely transparent about the data we collect and what we do with it.

**Can I opt out?**

Yes, you can. Since no personally identifiable information is being captured, we'd appreciate it if you let the script run; however if you are unhappy with the idea, simply run the following commands from the terminal window after creating the workspace, and this will remove the uptime script:

```
pkill uptime.sh
rm .vscode/uptime.sh
```
