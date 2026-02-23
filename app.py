import streamlit as st
from datetime import datetime
from PIL import Image
import os
import re
from supabase import create_client

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Project Spider Bot Registration",
    page_icon="🕷️",
    layout="centered"
)

# ---------------- SUPABASE CONNECTION ----------------
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------- HEADER ----------------
st.title("Project Spider Bot")
st.subheader("Robotics & Intelligent Systems Initiative")

st.markdown("""
Welcome to the official registration portal for **Project Spider Bot**.

If you're interested in collaborating on this robotics initiative,
please submit your details below.
""")

# ---------------- IMAGE (OPTIONAL) ----------------
image_path = "spider_bot.jpg"

if os.path.exists(image_path):
    image = Image.open(image_path)
    st.image(image, use_container_width=True)

# ---------------- PROJECT DETAILS ----------------
st.header("About the Project")

st.write("""
Project Spider Bot focuses on designing and developing
a modular multi-legged robotic system integrating:

- Robotics engineering  
- Embedded systems  
- Intelligent control systems  
- Real-time decision-making  
""")

# ---------------- VALIDATION FUNCTIONS ----------------
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

def is_valid_phone(phone):
    pattern = r"^\d{10}$"
    return re.match(pattern, phone)

# ---------------- RESPONSE SECTION ----------------
st.header("Your Response")

if "accepted" not in st.session_state:
    st.session_state.accepted = False

# ---------- DECLINE ----------
if st.button("Not Interested"):

    with st.form("decline_form"):
        name_decline = st.text_input("Full Name *")
        submit_decline = st.form_submit_button("Confirm")

        if submit_decline:

            if not name_decline.strip():
                st.error("Name is required.")
            else:
                supabase.table("invitations").insert({
                    "name": name_decline,
                    "email": "",
                    "phone": "",
                    "message": "",
                    "status": "Declined",
                    "submitted_at": datetime.now().isoformat()
                }).execute()

                st.success("Your response has been recorded.")
                st.stop()

# ---------- ACCEPT ----------
if st.button("Register / Accept Invitation"):
    st.session_state.accepted = True

# ---------------- REGISTRATION FORM ----------------
if st.session_state.accepted:

    st.success("Please complete the registration form.")

    with st.form("registration_form"):

        name_input = st.text_input("Full Name *")
        email = st.text_input("Email Address *")
        phone = st.text_input("Phone Number * (10 digits)")
        message = st.text_area("Optional Message")

        submit = st.form_submit_button("Submit Registration")

        if submit:

            errors = []

            # Required fields
            if not name_input.strip():
                errors.append("Name is required.")

            if not email.strip():
                errors.append("Email is required.")

            if not phone.strip():
                errors.append("Phone number is required.")

            # Format checks
            if email and not is_valid_email(email):
                errors.append("Invalid email format.")

            if phone and not is_valid_phone(phone):
                errors.append("Phone number must be exactly 10 digits.")

            if errors:
                for error in errors:
                    st.error(error)
            else:
                supabase.table("invitations").insert({
                    "name": name_input,
                    "email": email,
                    "phone": phone,
                    "message": message,
                    "status": "Accepted",
                    "submitted_at": datetime.now().isoformat()
                }).execute()

                st.success("Registration successful. Thank you!")
                st.balloons()

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Project Lead: Your Name | Project Spider Bot")