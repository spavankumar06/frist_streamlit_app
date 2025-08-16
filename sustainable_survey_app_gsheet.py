# sustainable_survey_with_gsheet.py
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import qrcode
from io import BytesIO

# -------------------- Google Sheets Setup --------------------
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Sustainable Survey Responses").sheet1

# -------------------- Survey Questions --------------------
questions = [
    {"q": "Do you use renewable energy at home?", "type": "single",
     "options": {"Yes, fully": 4, "Partially": 2, "No": 0, "Not sure": 0}},
    {"q": "How do you usually commute?", "type": "single",
     "options": {"Cycling/Walking": 4, "Electric/Hybrid car": 3, "Public transport": 2, "Car (petrol/diesel)": 0}},
    {"q": "How often do you recycle paper, plastic, glass, or metals?", "type": "single",
     "options": {"Always": 4, "Often": 3, "Sometimes": 2, "Never": 0}},
    {"q": "Do you compost food or garden waste?", "type": "single",
     "options": {"Yes": 4, "Planning to start": 2, "No": 0}},
    {"q": "When shopping, do you...", "type": "multi",
     "options": {"Bring reusable bags": 1, "Buy minimal packaging": 1, "Choose eco-friendly brands": 1, "None of the above": 0}},
    {"q": "How often do you eat locally grown or seasonal produce?", "type": "single",
     "options": {"Always": 4, "Often": 3, "Sometimes": 2, "Rarely": 0}},
    {"q": "Do you use water-saving devices?", "type": "single",
     "options": {"Yes": 4, "Not sure": 2, "No": 0}},
    {"q": "Have you participated in environmental programs or clean-ups?", "type": "single",
     "options": {"Yes": 4, "No": 0}}
]

# -------------------- Streamlit UI --------------------
st.set_page_config(page_title="Sustainable Lifestyle Survey", page_icon="🌱", layout="centered")
st.title("🌱 Sustainable Lifestyle Survey")
st.write("Answer the questions to see your Sustainability Score!")

score = 0
answers = []

with st.form("survey_form"):
    for idx, q in enumerate(questions):
        st.markdown(f"**{idx+1}. {q['q']}**")
        if q["type"] == "single":
            choice = st.radio("", list(q["options"].keys()), key=idx)
            answers.append(choice)
            score += q["options"][choice]
        elif q["type"] == "multi":
            choices = st.multiselect("", list(q["options"].keys()), key=idx)
            answers.append(", ".join(choices))
            for c in choices:
                score += q["options"][c]
    submitted = st.form_submit_button("Submit")

# -------------------- Store in Google Sheet --------------------
if submitted:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for q, a in zip(questions, answers):
        sheet.append_row([timestamp, q["q"], a, score])
    st.success(f"Your Sustainability Score: {score}")

    # Category
    if score >= 30:
        st.success("🌟 Sustainability Star – keep leading the way!")
    elif score >= 20:
        st.info("🌿 On the Right Path – great work, keep improving!")
    else:
        st.warning("🌎 Room to Grow – start with small, daily changes!")

# -------------------- Generate QR Code for Hosted Link --------------------
if st.button("Generate QR Code for this Survey"):
    hosted_link = "https://sustainablesurveyapp2025.streamlit.app/"  # Replace with actual deployed link
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(hosted_link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="green", back_color="white")

    buf = BytesIO()
    img.save(buf)
    st.image(buf.getvalue(), caption="Scan to Take the Survey")
