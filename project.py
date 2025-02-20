import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from twilio.rest import Client
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import pywhatkit
import time

# Initialize Firebase Admin SDK
cred = credentials.Certificate("path_to_your_firebase_service_account.json") #Add path to JSON file 
firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()
collection_name = "coll_name" #Name of collection acc to your firebase.

# Twilio SMS configuration
account_sid = "YOUR_TWILIO_ACCOUNT_SID"
auth_token = "YOUR_TWILIO_AUTH_TOKEN"
twilio_phone_number = "+YOUR_TWILIO_PHONE_NUMBER"

twilio_client = Client(account_sid, auth_token)


# Email configuration
sender_email = "your_email@gmail.com"
app_password = "your_gmail_app_password" # Gmail app password

# Interval for fetching data
interval_seconds = 15 #Change according to needs

# Function to send email
def send_email(receiver_email, patient_name, systolic, diastolic):
    print("Sending Mail....")
    subject = "BP Alert: Abnormal Reading Detected"
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    body = f"""
    Hello ,

    This is to inform you that {patient_name} has an abnormal BP reading:
    - Systolic: {systolic} mmHg
    - Diastolic: {diastolic} mmHg

    Please take the necessary actions.

    Best regards,
    Patient Monitoring System
    """

    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print(f"Email sent to {receiver_email} successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to send SMS
def send_sms(to_number, patient_name, systolic, diastolic):
    print("Sending SMS....")
    message_body = f"Alert: {patient_name} has an abnormal BP reading. Systolic: {systolic} mmHg, Diastolic: {diastolic} mmHg. Please check immediately."
    try:
        message = twilio_client.messages.create(
            to=to_number,
            from_=twilio_phone_number,
            body=message_body
        )
        print(f"SMS sent to {to_number} successfully! SID: {message.sid}")
    except Exception as e:
        print(f"Error sending SMS: {e}")

# Function to send WhatsApp message
def send_whatsapp_message(phone_number, patient_name, systolic, diastolic):
    print("Sending Whatsapp Msg....")
    message = f"Alert: {patient_name} has an abnormal BP reading. Systolic: {systolic} mmHg, Diastolic: {diastolic} mmHg. Please take necessary action."
    try:
        pywhatkit.sendwhatmsg(phone_number, message)
        print(f"WhatsApp message sent to {phone_number} successfully!")
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")

# Function to display patient card
def display_patient_card(data):
    systolic = data.get("Systolic")
    diastolic = data.get("Diastolic")
    patient_name = data.get("Name")
    email = data.get("Email")
    age = data.get("Age")
    guardian_name = data.get("Guardian_Name")
    guardian_phone = data.get("Guardian_Phone")
    guardian_email = data.get("Guardian_Mail")
    timestamp = data.get("Timestamp")
    is_abnormal = (systolic > 150) or (diastolic > 80)
    
    card_color = "#FFCDD2" if is_abnormal else "#C8E6C9"
    text_color = "#B71C1C" if is_abnormal else "#1B5E20"
    status_message = "BP is within normal range." if not is_abnormal else "Alert: BP is abnormal. Notification sent to guardian."

    card_html = f"""
        <div style='background-color: {card_color}; padding: 20px; border-radius: 15px; width: 90%; margin: auto;'>
            <h2 style='color: {text_color};'>{patient_name}</h2>
            <p><strong>Age:</strong> {age}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Readings taken on:</strong> {timestamp}</p>
            <p><strong>Systolic:</strong> <span style='color: {text_color}; font-weight: bold;'>{systolic} mmHg</span></p>
            <p><strong>Diastolic:</strong> <span style='color: {text_color}; font-weight: bold;'>{diastolic} mmHg</span></p>
            <hr>
            <h4>Guardian Contact</h4>
            <p><strong>Name:</strong> {guardian_name}</p>
            <p><strong>Mobile:</strong> {guardian_phone}</p>
            <p><strong>Email:</strong> {guardian_email}</p>
            <p style='margin-top: 15px; font-weight: bold; color: {text_color};'>{status_message}</p>
        </div>
    """
    return card_html

# Function to fetch the most recent BP records and display on Streamlit
def fetch_and_display_records():
    placeholder = st.empty()  # Placeholder to clear and update content
    with placeholder.container():
        docs = db.collection(collection_name).order_by("Timestamp", direction=firestore.Query.DESCENDING).limit(2).stream()
        
        cards = []
        for doc in docs:
            data = doc.to_dict()
            print(f"Fetched Data streamlit: {data}")
            card_html = display_patient_card(data)
            cards.append(card_html)

        col1, col2 = st.columns(2)
        if len(cards) > 0:
            with col1:
                st.markdown(cards[0], unsafe_allow_html=True)
        if len(cards) > 1:
            with col2:
                st.markdown(cards[1], unsafe_allow_html=True)

        # Check and send notifications for abnormal readings
        for data in [doc.to_dict() for doc in docs]:
            if (data.get("Systolic") and data.get("Systolic") > 150) or (data.get("Diastolic") and data.get("Diastolic") > 80):
                send_email(data.get("Guardian_Mail"), data.get("Name"), data.get("Systolic"), data.get("Diastolic"))
                send_sms(data.get("Guardian_Phone"), data.get("Name"), data.get("Systolic"), data.get("Diastolic"))
                send_whatsapp_message(data.get("Guardian_Phone"), data.get("Name"), data.get("Systolic"), data.get("Diastolic"))

# Streamlit App Layout
st.title("Patient BP Monitoring Dashboard")
st.write("Monitoring patients' BP and notifying guardians in case of abnormalities.")

# Auto-refresh to keep data updated
while True:
    fetch_and_display_records()
    time.sleep(interval_seconds)
