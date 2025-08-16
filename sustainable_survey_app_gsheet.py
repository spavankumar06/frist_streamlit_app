import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import qrcode
from io import BytesIO
from PIL import Image

# ----------------------
# CONFIG - UPDATE THESE
# ----------------------
SPREADSHEET_NAME = "Sustainability Responses"
CREDENTIALS_FILE = "credentials_json.json"  # Path to your Google API JSON key
SURVEY_LINK = "https://surabhisustainablesurveyappgrade6.streamlit.app/"  # Update after hosting

# ----------------------
# GOOGLE SHEETS SETUP
# ----------------------
scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scopes)
client = gspread.authorize(creds)
sheet = client.open(SPREADSHEET_NAME).sheet1

# ----------------------
# SURVEY QUESTIONS
# ----------------------
questions = [
    ("How often do you use public transport?", {"Always": 5, "Sometimes": 3, "Never": 0}),
    ("Do you recycle household waste?", {"Always": 5, "Sometimes": 3, "Never": 0}),
    ("How often do you use reusable bags?", {"Always": 5, "Sometimes": 3, "Never": 0}),
    ("Do you conserve electricity at home?", {"Always": 5, "Sometimes": 3, "Never": 0}),
    ("How often do you buy locally produced goods?", {"Always": 5, "Sometimes": 3, "Never": 0})
]

# ----------------------
# STREAMLIT UI
# ----------------------
st.title("♻️ Sustainable Lifestyle Survey - Australia")
st.write("Help us understand how sustainable your lifestyle is. Your answers will help promote eco-friendly initiatives.")

name = st.text_input("Full Name")
email = st.text_input("Email Address")

answers = []
score = 0

for q, opts in questions:
    choice = st.radio(q, list(opts.keys()), key=q)
    answers.append(choice)
    score += opts[choice]

if st.button("Submit Survey"):
    if not name or not email:
        st.error("Please fill in your name and email.")
    else:
        sheet.append_row([name, email] + answers + [score])
        st.success(f"Thank you {name}! Your sustainability score is {score} / {len(questions)*5}.")

# ----------------------
# QR CODE GENERATION
# ----------------------
if st.button("Generate Survey QR Code"):
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(SURVEY_LINK)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="#228B22", back_color="white")  # Forest green
    buf = BytesIO()
    img.save(buf)
    buf.seek(0)
    
    st.image(img, caption="Scan to take the survey")
    st.download_button(
        label="Download QR Code",
        data=buf,
        file_name="sustainability_survey_qr.png",
        mime="image/png"
    )
