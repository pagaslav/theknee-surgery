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

### Admin

As the site admin, I have the following capabilities:

1. Accept appointment requests from patients and assign them to specific doctors.
2. View and edit the profiles and information of any user on the site.
3. View a list of all users.
4. Delete users or reset their passwords.
5. Add new doctors.

### Doctor

As a doctor, I have the following capabilities:

1. Receive appointment requests from the admin for specific patients and schedule these appointments for specific dates and times.
2. View patient profiles.
3. Delete patient appointment requests.
4. Add, edit, and update medical records obtained during appointments with patients.

## User Experience (UX) &

User Interface (UI)

### Wireframes

<details>
<summary>Home Page</summary>

![Home Page](static/documentation/wireframes/home-page.webp)
</details>

<details>
<summary>Log in Page</summary>

![Log in Page](static/documentation/wireframes/login-page.webp)
</details>

<details>
<summary>Sign Up Page</summary>

![Sign Up Page](static/documentation/wireframes/signup-page.webp)
</details>

<details>
<summary>Our Doctors Page</summary>

![Our Doctors Page](static/documentation/wireframes/our-doctors-page.webp)
</details>

<details>
<summary>About Us Page</summary>

![About Us Page](static/documentation/wireframes/about-us-page.webp)
</details>

<details>
<summary>Privacy Policy Page</summary>

![Privacy Policy Page](static/documentation/wireframes/privacy-polisy-page.webp)
</details>

<details>
<summary>Profile Page</summary>

![Profile Page](static/documentation/wireframes/profile-page.webp)
</details>

<details>
<summary>Add Doctor Page</summary>

![Add Doctor Page](static/documentation/wireframes/add-doctor-page.webp)
</details>

<details>
<summary>All Users Page</summary>

![All Users Page](static/documentation/wireframes/all-users-page.webp)
</details>

<details>
<summary> Medical Records Page</summary>

![Medical Records Page](static/documentation/wireframes/medical-record-page.webp)
</details>

<details>
<summary>Map of website</summary>

![Map of website](static/documentation/wireframes/map.webp)

</details>



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

Our website utilises a combination of modern and visually appealing fonts to enhance readability and user experience. We have integrated two main fonts, “Bebas Neue” and “Oswald”, which are imported from Google Fonts. These fonts are selected to create a clean and professional look, making the content easily digestible for our users.

#### Font Usage:

##### Bebas Neue:

- **Logo**: The site logo, defined under the .logo-setup and .navbar-brand classes, uses Bebas Neue to create a distinct and bold appearance.

- **Headings**: Main headings, such as the welcome title on the index page (.welcome-title), utilise Bebas Neue to make a strong visual impact.

##### Oswald:

- **Body Text**: The primary font for body text is Oswald. This includes the general text across the site, defined in the body tag. The font settings ensure a clean and readable design with font-weight: 300 and font-size: 17px.
- **Subtitles and Minor Headings**: Subtitles and minor headings, such as the welcome subtitle (.welcome-subtitle) and welcome text (.welcome-text), also use Oswald. These elements are styled with specific font sizes and transformations to maintain a cohesive look.
- **Forms and Buttons**: Text within forms and buttons, such as those on the login and signup pages, use Oswald to ensure readability and consistency throughout the user interface.

[**Font Awesome**](https://fontawesome.com/) icons were used throughout the site. These are useful for making buttons, input fields, and links clear for the user.

By using these fonts strategically, we aim to provide a cohesive and visually appealing user experience that enhances both readability and the overall aesthetic of the website.

### The Knee surgery Logo
The logo for The Knee Surgery clinic is designed to be both professional and approachable, reflecting the clinic’s commitment to high-quality care and patient comfort.

## Features

### Navigation
The navigation panel of The Knee Surgery clinic website is designed to provide a user-friendly and intuitive browsing experience.

#### Navbar
The Navbar section is designed with both aesthetics and functionality in mind. Below is a detailed breakdown of its features:

##### Additional Features

- **Clock and Date Display**: 
  - Above the navigation panel, you will find a clock and date display. This helps users keep track of the current time while browsing the site.

- **Future Search Bar**: 
  - As the website grows, a search bar will be added above the navigation panel. This will allow users to search for various information on the site. 
  - Although we planned to include this feature in the current project, we ran out of time.

##### Navigation Panel

- **Position and Behavior**: 
  - The navigation panel is located at the top of the page.
  - For design reasons, it does not remain fixed during scrolling.
  - As you scroll down, a back-to-top arrow appears in the bottom right corner. This arrow remains dynamically positioned as you scroll, allowing easy navigation back to the top of the page.

##### Layout and Responsiveness

- **Logo Placement**: 
  - The logo is situated on the left side of the navigation panel.

- **Menu Items**: 
  - The menu items, which change based on user authentication status, are located on the right side of the panel.
  - As the screen size decreases, the menu items and the logo first move towards the center. Eventually, the menu items transform into a hamburger menu, thanks to Bootstrap classes.

##### Menu Item Descriptions

- **Intuitive Labels**: 
  - The pages linked by the menu items are self-explanatory based on their labels.

##### Desktop View:

![Desktop View](static/documentation/navbar/desktop-navbar.webp)

##### Responsive Design:

##### Tablet View:

![Tablet View](static/documentation/navbar/tablet-close-navbar.webp)
![Tablet View](static/documentation/navbar/tablet-open-navbar.webp)

##### Mobile View:

![Mobile View](static/documentation/navbar/mob-close-navbar.webp)
![Mobile View](static/documentation/navbar/mob-open-navbar.webp)

### Footer

The footer section of our website is designed to provide essential information and easy access to our social media channels. Below is a detailed description of its features and layout across different devices:

##### Desktop View:

![Desktop View](static/documentation/footer/footer-desktop.webp)

- **Logo and Company Name**: 
  - Located on the left side of the footer, the company logo and name, "THE KNEE SURGERY," are prominently displayed.

- **Contact Information**: 
  - In the center, visitors can find our contact details:
    - **Address**: 456 Side Street, Cardiff, CF19 6FY
    - **Email**: theknee.surgery@gmail.com

- **Social Media Icons**: 
  - To the right, icons for Instagram, Facebook, Twitter, and YouTube are displayed, providing quick links to our social media profiles.

- **Copyright and Privacy Policy**:
  - At the bottom, it states: "© 2024 Artem Bryzh. All rights reserved." 
  - A link to the Privacy Policy is also provided.

##### Responsive Design:

##### Tablet View:

![Tablet View](static/documentation/footer/footer-tablet.webp)

- **Logo and Company Name**: 
  - Located centrally.

- **Contact Information**:
  - Positioned centrally with the same details as the desktop view.

- **Social Media Icons**:
  - Aligned below the contact information, allowing easy access.

- **Back to Top Arrow**:
  - A convenient back-to-top arrow is present, aiding navigation.

##### Mobile View:

![Mobile View](static/documentation/footer/footer-mob.webp)

- **Logo and Company Name**: 
  - The company logo and name remain at the top, positioned centrally, ensuring brand visibility.

- **Contact Information**: 
  - Centrally aligned for easy reading.

- **Social Media Icons**: 
  - Arranged below the contact information in a horizontal layout.

- **Back to Top Arrow**:
  - Located at the bottom right corner, this arrow aids in easy navigation back to the top of the page.

The footer is designed to be responsive and user-friendly across all devices, ensuring that visitors can easily find contact information and access our social media channels, no matter the device they are using.

### Home Page
Welcome to The Knee Surgery homepage, designed with user experience and functionality in mind. Here’s a breakdown of its features:

![Home Page](static/documentation/pages/home-page-full.webp)

- **Introduction Section**: 
  - Contains a brief overview of our commitment to knee surgery and patient care.
  - Includes two prominent buttons for easy navigation: "Our Doctors" and "About Us"

- **Future Interactive Image**: 
  - A placeholder image that will be interactive in future updates, enhancing user engagement and providing more information visually.

- **Comprehensive List of Services**:
  - **Initial Consultation and Diagnosis**: Personalized assessment plans.
  - **Arthroscopic Surgery**: Minimally invasive procedures.
  - **Knee Replacement**: Advanced techniques and implants.
  - **Ligament Reconstruction**: Restoring knee stability.
  - **Physical Therapy and Rehabilitation**: Customized exercise programs.
  - **Injection Procedures**: Non-surgical pain management options.

### Log In Page
The Log In page allows users to access their accounts on The Knee Surgery website. The page includes the following features:

![Log In Page](static/documentation/pages/login-page-full.webp)

1. **Email Input**: Users enter their email address in a floating label input field.
2. **Password Input**: Users enter their password in a floating label input field.
3. **Remember Me Checkbox**: Users can choose to stay logged in for 30 days.
4. **Sign In Button**: Submits the form to log in the user.
5. **Sign Up Link**: Redirects new users to the sign-up page.
6. **Forgot Password**: Provides the administrator's email for password reset assistance.

When the "Sign In" button is clicked, the user's credentials are validated on the backend. If the credentials are correct, the user is logged in; otherwise, a flash message indicates incorrect email or password.

![Log In Incorrect](static/documentation/pages/login-page-incorrect.webp)

The "Remember Me" checkbox is processed on the backend. The backend code uses Flask session management to keep the user logged in if the checkbox is selected.

      ```python
      from flask import session

      # Session configuration
      app.config["SESSION_PERMANENT"] = False  # Session is not permanent by default
      app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=30)

      if existing_user:
              # Set session to be permanent if remember me is checked
              if remember:
                  # This sets the session to use the permanent lifetime
                  session.permanent = True
                  # Set session lifetime to 30 days
                  app.permanent_session_lifetime = timedelta(days=30)

Clicking on the administrator’s email opens the mail program with the “To” field filled out. 

### Sign Up Page
The sign-up page allows new users to create an account on The Knee Surgery website. The form includes client-side validation using JavaScript to ensure the password meets the criteria and matches the confirmation password. The backend handles additional validation, password hashing, and user creation.

![Sign Up Page](static/documentation/pages/signup-page-full.webp)

The page includes the following features:

1. **Full Name Input**: Users enter their full name in a floating label input field.
2. **Gender Selection**: Users select their gender from a dropdown list.
3. **Date of Birth Input**: Users enter their date of birth in a floating label input field.
4. **Phone Number Input**: Users enter their phone number, which must be between 9 to 11 digits. JavaScript handles input changes to show or hide a sample text.
5. **Email Input**: Users enter their email address in a floating label input field.
6. **Password Input**: Users create a password with requirements displayed below the input field. The password must be at least 8 characters long, contain an uppercase letter, and a number. JavaScript validates the password in real-time. Gray check marks turn green as each requirement is met.

![All marks are neutral](static/documentation/pages/signup-page-password-1.webp)

![One mark is green](static/documentation/pages/signup-page-password-2.webp)

![Two marks are green](static/documentation/pages/signup-page-password-3.webp)

![All marks are green](static/documentation/pages/signup-page-password-4.webp)

7. **Confirm Password Input**: Users confirm their password. JavaScript ensures that both password fields match. Each password field includes a Font Awesome eye icon that toggles password visibility when clicked.

![Visibility](static/documentation/pages/signup-page-password-5.webp)

8. **Terms and Conditions Checkbox**: Users must agree to the terms and conditions. Clicking the link opens a modal with the terms for review.

![Terms and Conditions](static/documentation/pages/signup-page-terms.webp)

Users must agree to the terms and conditions. Without checking this box, users cannot complete the registration.

![Terms and Conditions agree](static/documentation/pages/signup-page-terms-checkbox.webp)

On the backend, the following occurs:

- **Email Validation**: The backend checks if the email is already registered.
- **Password Validation**: The backend ensures the passwords match and meet the requirements.
- **Password Hashing**: The password is hashed using `generate_password_hash`.
- **User Creation**: A new user record is created and saved in the database.
- **Session Handling**: The user's email is added to the session to log them in automatically.

### Privacy Policy Page
The Privacy Policy page provides detailed information about how The Knee Surgery website collects, uses, and protects user data. It is a crucial component for informing users about their privacy rights and the measures taken to safeguard their information. 

<details>
<summary>See Privacy policy Page</summary>

![Privacy Policy Page](static/documentation/pages/policy-page-full.webp)
</details><br>
  
The policy includes sections on:

- **Data Collection**: Explains what personal data is collected, such as email addresses, names, phone numbers, and usage data.
- **Usage of Data**: Describes how the collected data is used to provide and improve services.
- **Cookies and Tracking**: Details the use of cookies and other tracking technologies to enhance user experience.
- **Data Sharing**: Outlines conditions under which user data may be shared with third parties.
- **Data Security**: Ensures the protection of personal data, though it acknowledges no method is 100% secure.
- **Children’s Privacy**: States the service does not address users under 13 and the measures taken if such data is inadvertently collected.
- **External Links**: Advises users to review privacy policies of linked websites not operated by The Knee Surgery.
- **Policy Changes**: Notifies users that the Privacy Policy may be updated and the process for informing users of changes.

This Privacy Policy was generated and adapted using the [Privacy Policy Generator](https://www.termsfeed.com/privacy-policy-generator/).

### Our Doctors Page
The "Our Doctors" page features images and brief information about our doctors, including their specialties and experience. This page dynamically updates with new doctors added by the admin through a for loop, ensuring the latest information is always displayed.

![Our Doctors Page](static/documentation/pages/our-doctors-page-full.webp)

The page layout includes:

- **Doctor Image**: Displays the doctor's image if available; otherwise, a default image is shown.
- **Doctor Information**: Presents the doctor's name, specialty, description, and additional information.

The page structure is generated automatically from the database entries using the following template code snippet:

      ```html
      {% for doctor in doctors %}
      <div class="col-12">
        <div class="card mb-3">
          <div class="row g-0">
            <div class="col-md-4">
              <img
                src="{{
                  url_for('static', filename=get_image_path(doctor.image)) 
                  if doctor.image else
                  url_for('static', filename='images/default-doctor.webp') 
                }}"
                class="img-fluid rounded-start"
                alt="{{ doctor.name }}">
            </div>
            <div class="col-md-8">
              <div class="card-body">
                <h3 class="card-title">{{ doctor.name }}</h3>
                <p class="card-text">{{ doctor.specialty }}</p>
                <p class="card-text">{{ doctor.description }}</p>
                <p class="card-text-hide">{{ doctor.additional_info }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      {% endfor %}

### About us Page
The "About Us" page for The Knee Surgery website provides comprehensive information about the clinic, its history, and its commitment to providing high-quality orthopedic care.

- **Introduction**
  - A welcoming message with a brief history and the clinic's dedication to patient satisfaction and medical excellence.

![About Us Page](static/documentation/pages/about-us-page-full.webp)

- **Carousel Section**
  - A Bootstrap carousel showcasing four key areas of the clinic:
    1. **Reception at Our Clinic**: Warm and inviting environment for patients.
    2. **Our Hospital Corridor**: Modern and convenient clinic facilities.
    3. **Operating Theatre**: Equipped with the latest medical technology.
    4. **Hospital Room**: Comfortable and modern environment for patients.

For optimal viewing experience, different images are used for various screen sizes, ensuring clarity and quality on all devices.

**Detailed Descriptions**
  - **Our Journey**: The history of the clinic and its growth over the past decade.
  - **Our Commitment to Quality**: Focus on personalized treatment plans and understanding patient needs.
  - **Patient Satisfaction**: Testimonials and the dedication of the staff to provide excellent care.
  - **Continuous Improvement**: Ongoing training and certification programs for doctors.
  - **Our Community**: Involvement in the local community through health fairs and educational seminars.
  - **Looking to the Future**: Commitment to innovation and expanding services.

As we continue to grow and evolve, we are excited to share that we have plans to enhance our “About Us” page further. In the near future, we aim to include testimonials from our patients, offering firsthand accounts of their experiences and the positive impact our clinic has had on their lives. These testimonials will provide valuable insights and reinforce the trust and satisfaction our patients feel.

Additionally, we will be showcasing our certifications and achievements in the medical field. By highlighting the qualifications and accolades of our dedicated team, we aim to demonstrate our commitment to excellence and continuous improvement. These additions will give visitors a more comprehensive understanding of our clinic’s dedication to providing exceptional orthopedic care.

### Profile Page

#### Patient Profile Page

The patient profile page on our website offers a comprehensive view of the patient's personal information, medical records, and appointment management. Here is an overview of what the patient can do and see on this page:

![Patient Profile Page](static/documentation/pages/profile-patient-page.webp)

##### Key Sections:

1. **User Information**
   - **Name:** Displays the patient's name, with an option to edit.
   - **Role:** Shows the user's role as a patient.
   - **Phone:** Shows the patient's phone number, with an option to edit.
   - **Email:** Displays the patient's email, with an option to edit.
   - **Gender:** Shows the patient's gender.
   - **Date of Birth:** Displays the patient's date of birth.

2. **Change Password**
   - Patients can change their password by providing the current password and setting a new one, ensuring it meets security requirements.

3. **Medical Records**
   - **List of Medical Records:** Displays detailed information about the patient's medical history, including descriptions, treatments, dates, and the attending doctor's details.
   - **Download and Delete Files:** Patients can view, download, and delete their uploaded files related to their medical records.

4. **Scheduled Appointments**
   - **View Scheduled Appointments:** Displays the list of upcoming appointments with doctors, including the doctor's name, reason for the visit, and scheduled date and time.

5. **Requested Appointments**
   - **List of Appointment Requests:** Shows the appointments that the patient has requested, including the reason and current status of each request.

6. **Request an Appointment**
   - **Form to Request Appointments:** Allows patients to request new appointments by providing the reason for the visit.

This page is designed to be user-friendly, providing patients with easy access to their medical information and appointment management tools.

#### Admin Profile Page

The admin profile page on our website is designed to provide a comprehensive set of tools for managing user information, medical records, and appointments. Here's a breakdown of the key features and functionalities available to administrators:

![Admin Profile Page](static/documentation/pages/profile-admin-page.webp)

##### Key Sections:

1. **User Information**
   - **Name:** Displays the admin's name with an option to edit.
   - **Role:** Shows the user's role as an admin, with the ability to edit.
   - **Phone:** Displays the admin's phone number, which can be edited.
   - **Email:** Shows the admin's email address, with an option to update it.

2. **Change Password**
   - Admins can securely change their password by entering the current password and setting a new one, ensuring it meets security requirements.

3. **Appointment Requests**
   - **List of Appointment Requests:** Displays all pending appointment requests from patients, including the patient's name and the reason for the appointment.
   - **Assign Doctor:** Allows admins to assign doctors to specific appointment requests, facilitating efficient scheduling and management.

4. **Admin-Specific Actions**
   - **View All Users:** A button that navigates to a page where admins can view and manage all users and doctors in the system.
   - **Add a New Doctor:** A button that links to a form where admins can add new doctors, expanding the clinic's team.

5. **Uploaded Files**
   - **Manage Files:** Admins can view, download, and delete uploaded files related to patient records, ensuring all relevant documents are easily accessible.
   - **Upload Documents:** Provides a form for uploading new documents, with options to categorize the file type (e.g., medical record, analysis, profile picture, or other).

The admin profile page is designed to give administrators full control over the system, ensuring efficient management of user information, medical records, and appointments. This comprehensive toolset helps maintain the high standards of care and service at our clinic.

#### Doctor Profile Page

The doctor profile page on our website is designed to provide doctors with the tools and information they need to manage their patient interactions, appointments, and medical records efficiently. Here's a detailed overview of the key features and functionalities available to doctors:

![Doctor Profile Page](static/documentation/pages/profile-doctor-page.webp)

##### Key Sections:

1. **User Information**
   - **Name:** Displays the doctor's name with an option to edit.
   - **Role:** Shows the user's role as a doctor.
   - **Phone:** Displays the doctor's phone number, which can be edited.
   - **Email:** Shows the doctor's email address, with an option to update it.
   - **Specialty:** Displays the doctor's specialty, which can be updated to reflect their expertise.

2. **Change Password**
   - Doctors can securely change their password by entering the current password and setting a new one, ensuring it meets security requirements.

3. **Assigned Patients**
   - **List of Assigned Patients:** Displays all patients assigned to the doctor, including patient names, reasons for appointments, and symptoms.
   - **Accept and Schedule Appointments:** Allows doctors to accept and schedule appointments, providing fields for the appointment date and time.
   - **Medical Records:** Doctors can view and access the medical records of their assigned patients, ensuring they have all the necessary information for consultations.

4. **Medical Records Management**
   - **View Medical Records:** Provides detailed information about patients' medical records, including descriptions, treatments, and dates.
   - **Add Medical Record:** Doctors can add new medical records for their patients, documenting treatments, descriptions, and dates.

The doctor profile page is designed to give doctors full control over their interactions with patients, ensuring efficient management of patient information, medical records, and appointments. This comprehensive toolset helps maintain the high standards of care and service at our clinic.

### Appointment Request and Scheduling Workflow on Profile Page
This section describes the complete workflow for requesting and scheduling an appointment within the Knee Surgery application. It details the steps from a patient requesting an appointment to a doctor scheduling it, including the roles of the patient, admin, and doctor.

#### Step-by-Step Process:

1. **Patient Requests an Appointment:**
   - **Action:** The patient fills out the "Request an Appointment" form, specifying the reason for the appointment.

   ![Request an Appointment](static/documentation/pages/appointment/request-patient-1.webp)

   - **Interface:** The patient clicks the "Request Appointment" button.

   ![Click the button](static/documentation/pages/appointment/request-patient-2.webp)

2. **Page Reload and Confirmation:**
   - **Action:** Upon clicking the button, the page reloads.
   - **Interface:** The requested appointment appears in the patient's profile under the "Requested Appointments" section.

   ![Requested Appointments](static/documentation/pages/appointment/requested-patient.webp)

3. **Database Update:**
   - **Action:** The appointment request is added to the `theknee_surgery.appointments` collection in MongoDB.
   - **Details:** The new appointment entry includes a status of `pending`.

   ![MongoDB status of `pending`](static/documentation/pages/appointment/request-mongo-1.webp)

4. **Admin Views Appointment Request:**
   - **Action:** In the admin profile, the new appointment request is visible under the "Appointment Requests" section.
   - **Interface:** The request includes the patient's name, reason for the appointment, and an option to assign a doctor.

   ![Appointment Requests for admin](static/documentation/pages/appointment/request-admin.webp)

5. **Admin Assigns a Doctor:**
   - **Action:** The admin selects a doctor from a dropdown menu and clicks the "Assign Doctor" button.

   ![Assigns a Doctor](static/documentation/pages/appointment/assign-admin.webp)

   - **Database Update:** The status of the appointment in MongoDB changes from `pending` to `assigned`.

   ![MongoDB status of `assigned`](static/documentation/pages/appointment/assign-mongo.webp)

   - **Interface:** The appointment request is removed from the admin's "Appointment Requests" section and appears in the assigned doctor's profile under the "Assigned Patients" section.

   ![Assigned Patients for doctor](static/documentation/pages/appointment/assigned-doctor-1.webp)

6. **Doctor Schedules the Appointment:**
   - **Action:** The doctor selects a date and time for the appointment and clicks the "Accept and Schedule" button.

   ![Accept and Schedule](static/documentation/pages/appointment/assigned-doctor-2.webp)

   - **Database Update:** The status of the appointment in MongoDB changes to `scheduled`.

   ![MongoDB status of `scheduled`](static/documentation/pages/appointment/sheduled-mongo.webp)

7. **Updated Views for Doctor and Patient:**
   - **Doctor's Profile:**
   - **Interface:** The scheduled appointment remains in the "Assigned Patients" section.

   ![Assigned Patients](static/documentation/pages/appointment/assigned-doctor-3.webp)

   - **Patient's Profile:**
   - **Interface:** The appointment is moved from the "Requested Appointments" section to the "Scheduled Appointments" section with the assigned date and time.

   ![Scheduled Appointments](static/documentation/pages/appointment/sheduled-patient.webp)

### Database Collection:

- **Collection:** `theknee_surgery.appointments`
  - **Fields:**
    - `patient_id`: Reference to the patient requesting the appointment.
    - `doctor_id`: Reference to the doctor assigned to the appointment.
    - `reason`: Reason for the appointment.
    - `status`: Status of the appointment (`pending`, `assigned`, `scheduled`).
    - `appointment_datetime`: Date and time when the appointment is scheduled (added during the scheduling step).

### Workflow Summary:

1. **Patient Action:** Requests an appointment.
2. **System Action:** Adds request to database with status `pending`.
3. **Admin Action:** Assigns a doctor, changing status to `assigned`.
4. **Doctor Action:** Schedules the appointment, changing status to `scheduled`.
5. **Patient and Doctor Views:** Updated to reflect the current status and details of the appointment.

This workflow ensures a seamless process for managing appointment requests, assignments, and scheduling within the Knee Surgery application.


### All Users Page
The "All Users" page is an administrative tool that provides a detailed overview of all users registered on the website. This page is accessible exclusively to administrators and serves as a central hub for user management. Below is a detailed description of the features and functionalities available on the All Users page:

![All Users Page](static/documentation/pages/admin-users-page.webp)

#### Key Features:

1. **User List Overview:**
   - **Sorted Display:** The page displays all users in a sorted order, starting with administrators, followed by doctors, and then patients. This helps in quickly identifying and managing users based on their roles.
   - **User Information:** Each entry includes the user's full name and role, with a link to view their profile for more detailed information.

2. **Flash Messages:**
   - **Notifications:** The page includes a section for flash messages to notify the admin of the success or failure of various actions, such as password resets or user deletions.

3. **User Actions:**
   - **Reset Password:** Administrators can reset a user's password by generating a new random password, which is hashed and updated in the database. The new password is displayed to the admin for further communication to the user. This feature is particularly useful if a user forgets their password and requests access recovery.
   - **Delete User:** Administrators have the ability to delete any user from the system. This action requires confirmation to prevent accidental deletions.

#### User Management Workflow:

- **Accessing the Page:** The "All Users" page is linked from the admin's profile page, making it easily accessible for user management tasks.
- **Viewing Profiles:** Admins can click on a user's name to view their detailed profile, which provides more context and information about the user.
- **Performing Actions:** Admins can reset passwords or delete users directly from the All Users page, with appropriate confirmation prompts to ensure deliberate actions.

### Add Doctor Page
The "Add Doctor" page is a crucial tool for administrators to manage the medical staff at The Knee Surgery clinic. This page is exclusively accessible through the admin's profile and allows the admin to add new doctors to the database. Once added, these doctors are automatically displayed on the "Our Doctors" page.

![Add Doctor Page](static/documentation/pages/add-doctor-page.webp)

1. **Bootstrap Form:**
   - **User-Friendly Design:** The page features a Bootstrap form designed to be intuitive and user-friendly, ensuring that admins can quickly and easily add new doctors.

2. **Form Fields:**
   - **Full Name:** A required input field for the doctor's full name.
   - **Specialty:** A required input field for the doctor's specialty.
   - **Description:** A required textarea for a brief description of the doctor's role and activities.
   - **Additional Information:** An optional textarea for more detailed information about the doctor. This section is hidden on screens smaller than 600 pixels to ensure a clean and responsive design.
   - **Email:** A required input field for the doctor's email address.
   - **Password:** A required input field for setting the doctor's password.

3. **Backend Integration:**
   - **Form Submission:** When the form is submitted, the backend processes the input data. This includes validating the entries, hashing the password for security, and generating an image name based on the doctor's full name.
   - **Database Update:** The new doctor's information is saved to the MongoDB database, and the doctor is immediately added to the "Our Doctors" page.

4. **Security and Permissions:**
   - **Admin-Only Access:** The page and its functionalities are restricted to users with admin privileges. Non-admin users attempting to access the page are redirected with a permission error message.

### Medical Records Page
The Medical Record page is a comprehensive tool designed for doctors and admin users to manage and update patient medical records efficiently. This page provides a detailed view of the patient's medical history and allows for the upload and management of associated documents.

![Medical Record Page](static/documentation/pages/medical-record-page.webp)

#### Key Features:

1. **Flash Messages:**
   - **User Notifications:** At the top of the page, flash messages are displayed to inform users about the success or failure of their actions, such as updates or deletions.

2. **Medical Record Details:**
   - **Patient Information:** The patient's name is displayed in a read-only format.
   - **Record Date:** An input field for the date of the medical record.
   - **Description:** A textarea for the description of the medical record, pre-filled with existing data.
   - **Treatment:** A textarea for the treatment details, pre-filled with existing data.
   - **Update Button:** If the logged-in user is either the doctor assigned to the record or an admin, they can update the medical record.

3. **Uploaded Files Section:**
   - **List of Files:** Displays all files uploaded related to the medical record. Each file has a download link and a delete button.
   - **Delete Functionality:** Admins and the assigned doctor can delete any file associated with the medical record.

4. **Upload Document Section:**
   - **File Upload:** Allows users to upload new documents related to the medical record.
   - **Form Submission:** The form supports file uploads and sends the data to the backend for processing and storage.

#### Page Workflow:

- **Viewing Medical Records:** The page displays detailed information about a patient's medical history, including dates, descriptions, and treatments.
- **Uploading Files:** Users can upload new documents, such as test results or additional notes, to be associated with the medical record.
- **Updating Records:** Authorized users can update the medical record's details to reflect new information or changes in treatment.
- **Managing Files:** Users can view, download, or delete files that have been uploaded to the medical record.

### 404 Page
The **404 Page Not Found** is a user-friendly error page that is displayed when a user attempts to access a page that does not exist on the website. This page aims to inform users clearly and provide them with an easy way to navigate back to the homepage.

![404 Page](static/documentation/pages/404-page.webp)

#### Key Features:

1. **Title:**
   - **Page Title and subtitle:** The title of the page and subtitle is "404 The page you are looking for does not exist." making it immediately clear what the issue is.

2. **Content:**
   - **Error Code:** The page prominently displays the error code "404" in a large font size to catch the user's attention.
   - **Message:** A simple message informs the user that the page they are looking for does not exist.
   - **Navigation Button:** A button is provided to take the user back to the homepage, encouraging them to continue browsing the site.

#### Page Workflow:

- **User Interaction:** When a user lands on this page, they are informed of the error and given a clear option to return to the homepage.
- **Navigation:** The primary call-to-action is to direct the user back to a familiar place where they can continue their navigation without frustration.

### 403 Page
The **403 Forbidden** page is shown when a user attempts to access a page or resource they do not have permission to view. This could be due to various reasons, such as insufficient user privileges or restricted content.

![403 Page](static/documentation/pages/403-page.webp)

#### Key Features:

1. **Title:**
   - **Page Title and subtitle:** The title and subtitle of the page is "403 You do not have permission to access this page." clearly indicating the nature of the access issue.

2. **Content:**
   - **Error Code:** The error code "403" is displayed prominently in a large font size.
   - **Message:** A straightforward message informs the user that they do not have permission to access the requested page.
   - **Navigation Button:** A button is provided to return the user to the homepage, guiding them away from the restricted area.

#### Page Workflow:

- **User Interaction:** Users are immediately informed about the permission issue and are not left wondering why they cannot access the page.
- **Navigation:** The page encourages users to return to the homepage, providing a positive direction instead of a dead end.


## Technologies Used

- [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML) was used as the foundation of the site.
- [CSS](https://developer.mozilla.org/en-US/docs/Web/css) - was used to add the styles and layout of the site.
- [Bootstrap](https://getbootstrap.com/docs/5.3) was employed to integrate its styles, facilitating rapid development and
consistent styling across the pages.
- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) was employed to implement dynamic interactions on the site, enabling real-time user feedback and interactive features without needing to reload the page.
- [Python](https://www.python.org/)  is used as the back-end programming language.
- [Flask](https://flask.palletsprojects.com/en/3.0.x/) is the Python framework used for the site.
- [MongoDB](https://www.mongodb.com/) is the non-relational database management I chose to use for storing data.
- [VSCode](https://code.visualstudio.com/) was used as the main tool to write and edit code.
- [Git](https://git-scm.com/) was used for the version control of the website.
- [GitHub](https://github.com/) was used to host the code of the website.
- [GitHub Pages](https://pages.github.com/) was used for hosting the deployed front-end site.
- [Heroku](https://dashboard.heroku.com/apps)  is hosting the deployed back-end site.
- [Balsamiq](https://balsamiq.com/) was used to make wireframes for the website.
- [Adobe Photoshop](https://www.adobe.com/uk/products/photoshop.html) was used to make and resize images for the website and the
README file.
- [ICO Converter](https://www.icoconverter.com/) - for the favicon.
- [Chrome Developer Tools](https://developer.chrome.com/docs/devtools/) - was used to debug, to test responsiveness and generate Lighthouse reports.
- [Google Fonts](https://fonts.google.com/) - to import the site font.
- [Font Awesome](https://fontawesome.com/) - for all the site icons.
- [W3C HTML Validator](https://validator.w3.org/) - to test HTML code.
- [W3C CSS Validator](https://jigsaw.w3.org/css-validator) - to test the CSS code.
- [JSHint](https://jshint.com/) is a tool used to detect errors and potential problems in JavaScript code.

## Testing

### Responsiveness

<details>
<summary>Home Page</summary>

![Home Page](static/documentation/pages/responsiv/home-page-responsive.webp)
</details>

<details>
<summary>Log in Page</summary>

![Log in Page](static/documentation/pages/responsiv/login-page-responsive.webp)
</details>

<details>
<summary>Sign Up Page</summary>

![Sign Up Page](static/documentation/pages/responsiv/signup-page-responsive.webp)

With the opened Modal window:

![Sign Up Page with Modal](static/documentation/pages/responsiv/signup-1-page-responsive.webp)
</details>

<details>
<summary>Our Doctors Page</summary>

![Our Doctors Page](static/documentation/pages/responsiv/doctors-page-responsive.webp)
</details>

<details>
<summary>About Us Page</summary>

![About Us Page](static/documentation/pages/responsiv/about-page-responsive.webp)
</details>

<details>
<summary>Privacy Policy Page</summary>

![Privacy Policy Page](static/documentation/pages/responsiv/privacy-page-responsive.webp)
</details>

<details>
<summary>Profile Page</summary>

Patient

![Profile Page Patient](static/documentation/pages/responsiv/profil-patient-page-responsive.webp)

Admin

![Profile Page Admin](static/documentation/pages/responsiv/profil-admin-page-responsive.webp)

Doctor

![Profile Page Doctor](static/documentation/pages/responsiv/profil-doctor-page-responsive.webp)
</details>

<details>
<summary>Add Doctor Page</summary>

![Add Doctor Page](static/documentation/pages/responsiv/add-doctor-page-responsive.webp)
</details>

<details>
<summary>All Users Page</summary>

![All Users Page](static/documentation/pages/responsiv/all-users-page-responsive.webp)
</details>

<details>
<summary> Medical Records Page</summary>

![Medical Records Page](static/documentation/pages/responsiv/medical-record-page-responsive.webp)
</details>

<details>
<summary> 404 Page</summary>

![404 Page](static/documentation/pages/responsiv/404-page-responsive.webp)
</details>

<details>
<summary> 403 Page</summary>

![403 Page](static/documentation/pages/responsiv/403-page-responsive.webp)
</details>

### Validator testing

#### Python

I have used the recommended [PEP8 CI Python Linter](https://pep8ci.herokuapp.com/) to validate my Python file - app.py.

<details>

<summary> All clear, no errors found. See the screenshot</summary>

![404 Page](static/documentation/validator/ci-python-liner.webp)
</details>

#### HTML
I have used the recommended [HTML W3C Validator](https://validator.w3.org/) to validate all of my HTML files.

<details>
<summary>Home Page, no errors</summary>

![Home Page](static/documentation/validator/home-page-valid.webp)
</details>

<details>
<summary>Log in Page</summary>

![Log in Page](static/documentation/pages/responsiv/login-page-responsive.webp)
</details>

<details>
<summary>Sign Up Page</summary>

![Sign Up Page](static/documentation/pages/responsiv/signup-page-responsive.webp)

With the opened Modal window:

![Sign Up Page with Modal](static/documentation/pages/responsiv/signup-1-page-responsive.webp)
</details>

<details>
<summary>Our Doctors Page</summary>

![Our Doctors Page](static/documentation/pages/responsiv/doctors-page-responsive.webp)
</details>

<details>
<summary>About Us Page</summary>

![About Us Page](static/documentation/pages/responsiv/about-page-responsive.webp)
</details>

<details>
<summary>Privacy Policy Page</summary>

![Privacy Policy Page](static/documentation/pages/responsiv/privacy-page-responsive.webp)
</details>

<details>
<summary>Profile Page</summary>

Patient

![Profile Page Patient](static/documentation/pages/responsiv/profil-patient-page-responsive.webp)

Admin

![Profile Page Admin](static/documentation/pages/responsiv/profil-admin-page-responsive.webp)

Doctor

![Profile Page Doctor](static/documentation/pages/responsiv/profil-doctor-page-responsive.webp)
</details>

<details>
<summary>Add Doctor Page</summary>

![Add Doctor Page](static/documentation/pages/responsiv/add-doctor-page-responsive.webp)
</details>

<details>
<summary>All Users Page</summary>

![All Users Page](static/documentation/pages/responsiv/all-users-page-responsive.webp)
</details>

<details>
<summary> Medical Records Page</summary>

![Medical Records Page](static/documentation/pages/responsiv/medical-record-page-responsive.webp)
</details>

<details>
<summary> 404 Page</summary>

![404 Page](static/documentation/pages/responsiv/404-page-responsive.webp)
</details>

<details>
<summary> 403 Page</summary>

![403 Page](static/documentation/pages/responsiv/403-page-responsive.webp)
</details>

#### CSS

#### JavaScript

### LightHouse report

### Compatibility

### Manual Testing

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
![Bug 3, User not found Message](static/documentation/bugs/3/bug-3-1.webp)

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

![Bug 3, Result](static/documentation/bugs/3/bug-3-2.webp)

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

1. Doctor Illustrator Design, [License.](static/documentation/images/image-1-license-certificate.txt)
2. Physiotherapist check X ray, [License.](static/documentation/images/image-2-license-certificate.txt)
3. Hands operating a patient, [License.](static/documentation/images/image-3-license-certificate.txt)
4. Knee joint model , [License.](static/documentation/images/image-4-license-certificate.txt)
5. Ligament Reconstruction image was generated using AI from [ChatGPT](https://www.openai.com/chatgpt)
6. Bandaging woman's injured knee, [License.](static/documentation/images/image-6-license-certificate.txt)
7. Injection Procedures, [License.](static/documentation/images/image-7-license-certificate.txt)

#### Our Doctors page

1. Dr. John Doe photo, [License.](static/documentation/images/image-8-license-certificate.txt)
2. Dr. Jane Smith photo, [License.](static/documentation/images/image-9-license-certificate.txt)
3. Dr. Emily Johnson photo, [License.](static/documentation/images/image-10-license-certificate.txt)
4. Dr. Michael Brown photo, [License.](static/documentation/images/image-11-license-certificate.txt)

#### About Us page

1. Hospital reception counter, [License.](static/documentation/images/image-12-license-certificate.txt)
2. Busy Hospital Corridor, [License.](static/documentation/images/image-13-license-certificate.txt)
3. Modern operating theatre, [License.](static/documentation/images/image-14-license-certificate.txt)
4. A room of an hospital, [License.](static/documentation/images/image-15-license-certificate.txt)

## Acknowledgments

## Future Improvements