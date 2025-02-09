# **Patient Blood Pressure Monitoring and Alert System**

A real-time patient monitoring system that tracks blood pressure (BP) readings from **Cloud Database** and notifies guardians via **Email**, **SMS**, and **WhatsApp** when abnormal readings are detected. The project features a dynamic **Streamlit dashboard** to visualize patient data and alert statuses.

---

## **Table of Contents**

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Workflow](#project-workflow)
- [Potential Enhancements](#potential-enhancements)
- [License](#license)

---

## **Features**

- **Real-time Monitoring**: Fetches BP readings from Firestore cloud and updates every specified seconds.
- **Abnormal BP Detection**: Flags readings with **Systolic > 150 mmHg** or **Diastolic > 80 mmHg**.
- **Automated Notifications**:
  - **Email Alerts** via Gmail SMTP.
  - **SMS Alerts** using the Twilio API.
  - **WhatsApp Alerts** using PyWhatKit.
- **Dynamic Dashboard**: Color-coded patient cards to highlight abnormal readings.
- **Secure Integrations**: Utilizes Firebase Admin SDK, Twilio, and Gmail App Passwords for secure communication.

---

## **Technologies Used**

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Database**: [Firebase Firestore](https://firebase.google.com/docs/firestore)
- **Notifications**:
  - [Twilio](https://www.twilio.com/) for SMS
  - [smtplib](https://docs.python.org/3/library/smtplib.html) for Email
  - [PyWhatKit](https://pypi.org/project/pywhatkit/) for WhatsApp messaging
- **Python Libraries**:
  - `firebase_admin`
  - `twilio`
  - `pywhatkit`
  - `streamlit`

---

## **Installation**

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/KamaljeethAnand/PatientNotifSystem.git
   cd PatientNotifSystem
   ```

2. **Create a Virtual Environment (Optional but Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add Firebase Service Account Key:**
   - Download the service account JSON from your Firebase project settings.
   - Place it in the project directory and update the path in the code:
     ```python
     cred = credentials.Certificate("path_to_your_firebase_service_account.json")
     ```

---

## **Configuration**

1. **Firebase Firestore Setup**:
   - Create a **Firestore database** in your Firebase project.
   - Add a collection named `BP_records` with documents containing fields like:
     - `Name`, `Email`, `Systolic`, `Diastolic`, `Guardian_Name`, `Guardian_Phone`, `Guardian_Mail`, `Timestamp`.

2. **Twilio Configuration**:
   - Sign up on [Twilio](https://www.twilio.com/), create a project, and get your **Account SID** and **Auth Token**.
   - Replace in the script:
     ```python
     account_sid = "YOUR_TWILIO_ACCOUNT_SID"
     auth_token = "YOUR_TWILIO_AUTH_TOKEN"
     twilio_phone_number = "+YOUR_TWILIO_PHONE_NUMBER"
     ```

3. **Gmail SMTP Setup**:
   - Enable **2-Step Verification** on your Gmail account.
   - Generate an **App Password** and replace it in the script:
     ```python
     sender_email = "your_email@gmail.com"
     app_password = "your_gmail_app_password"
     ```

4. **WhatsApp Configuration (PyWhatKit)**:
   - Ensure your WhatsApp Web is logged in on your default browser.

---

## **Usage**

1. **Run the Streamlit App:**
   ```bash
   streamlit run project.py
   ```

2. **Dashboard Overview:**
   - The dashboard displays patient information, BP readings, and guardian contact details.
   - Color indicators:
     - **Red**: Abnormal BP (Alerts sent).
     - **Green**: Normal BP.

3. **Automatic Notifications:**
   - **Email**, **SMS** and **Whatsapp**  alerts are sent by default.
   - Comment the lines in `display_patient_card()` to disable any of the alerts:
     ```python
     send_email(guardian_email, patient_name, systolic, diastolic)
     send_sms(guardian_phone, patient_name, systolic, diastolic)
     send_whatsapp_message(guardian_phone, patient_name, systolic, diastolic)
     ```

---

## **Project Workflow**

1. **Initialization**:
   - Firebase Admin SDK, Twilio, and SMTP configurations are initialized.

2. **Data Fetching**:
   - BP records are fetched from the Firestore collection `BP_records`.

3. **Abnormal BP Detection**:
   - If **Systolic > 150 mmHg** or **Diastolic > 80 mmHg**, the system flags the reading as abnormal.

4. **Automated Notifications**:
   - Guardians receive alerts via Email, SMS, and WhatsApp.

5. **Real-time Dashboard Update**:
   - Patient data is updated on the Streamlit dashboard every **specific seconds**.

---

## **Potential Enhancements(NOT PART OF THIS PROJECT currenetly)**

- **Graphical Data Visualization**: Add BP trends over time using charts.
- **User Authentication**: Secure dashboard with login for healthcare professionals.
- **Custom Thresholds**: Personalize BP thresholds based on patient age or health history.
- **Two-Way Communication**: Allow guardians to acknowledge alerts.
- **Multi-Channel Notifications**: Integrate additional services like Slack or Telegram.

---

## **License**

This project is licensed under the [MIT License](LICENSE).

---

Feel free to adjust the links, repository name, or personal details based on your GitHub setup!

