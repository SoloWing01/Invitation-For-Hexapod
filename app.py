import streamlit as st
from datetime import datetime
from PIL import Image
import os
import re
from supabase import create_client

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Project Spider Bot",
    page_icon="🕷️",
    layout="centered"
)

# ---------------- SAFE SUPABASE CONNECTION ----------------
# (Keys stored securely in Streamlit Secrets)

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------- GET NAME FROM QR ----------------
params = st.query_params
name = params.get("invite", "Guest")

# ---------------- HEADER ----------------
st.title("Project Spider Bot")
st.subheader("Robotics & Intelligent Systems Initiative")

st.markdown(f"""
Hello **{name}**,  

You are invited to collaborate on **Project Spider Bot**, a professional robotics initiative focused on intelligent autonomous systems.
""")

# ---------------- IMAGE (OPTIONAL) ----------------
image_path = "spider_bot.jpg"

if os.path.exists(image_path):
    image = Image.open(image_path)
    st.image(image, use_container_width=True)

# ---------------- PROJECT DETAILS ----------------
st.header("About the Project")
st.write("""
Project Spider Bot aims to design and develop a modular robotic system inspired by multi-legged locomotion.

This initiative integrates robotics engineering, embedded systems, and intelligent control systems.
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
if st.button("Decline Invitation"):

    supabase.table("invitations").insert({
        "name": name,
        "email": "",
        "phone": "",
        "message": "",
        "status": "Declined",
        "submitted_at": datetime.now().isoformat()
    }).execute()

    st.success("Your response has been recorded.")
    st.stop()

# ---------- ACCEPT ----------
if st.button("Accept Invitation"):
    st.session_state.accepted = True

# ---------------- CONTACT FORM ----------------
if st.session_state.accepted:

    st.success("Please provide your contact details.")

    with st.form("contact_form"):

        email = st.text_input("Email Address *")
        phone = st.text_input("Phone Number * (10 digits)")
        message = st.text_area("Optional Message")

        submit = st.form_submit_button("Submit Details")

        if submit:

            errors = []

            # Required checks
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

                # Insert into Supabase
                supabase.table("invitations").insert({
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "message": message,
                    "status": "Accepted",
                    "submitted_at": datetime.now().isoformat()
                }).execute()

                st.success("Your information has been recorded successfully.")
                st.balloons()

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Project Lead: Your Name | Project Spider Bot")