# sustainable_survey_app.py
import streamlit as st

st.set_page_config(page_title="Sustainable Lifestyle Survey", page_icon="🌱", layout="centered")

st.title("🌱 Sustainable Lifestyle Survey")
st.write("Answer the questions to see your Sustainability Score!")

questions = [
    {
        "q": "Do you use renewable energy at home?",
        "type": "single",
        "options": {
            "Yes, fully": 4,
            "Partially": 2,
            "No": 0,
            "Not sure": 0
        }
    },
    {
        "q": "How do you usually commute?",
        "type": "single",
        "options": {
            "Cycling/Walking": 4,
            "Electric/Hybrid car": 3,
            "Public transport": 2,
            "Car (petrol/diesel)": 0
        }
    },
    {
        "q": "How often do you recycle paper, plastic, glass, or metals?",
        "type": "single",
        "options": {
            "Always": 4,
            "Often": 3,
            "Sometimes": 2,
            "Never": 0
        }
    },
    {
        "q": "Do you compost food or garden waste?",
        "type": "single",
        "options": {
            "Yes": 4,
            "Planning to start": 2,
            "No": 0
        }
    },
    {
        "q": "When shopping, do you...",
        "type": "multi",
        "options": {
            "Bring reusable bags": 1,
            "Buy minimal packaging": 1,
            "Choose eco-friendly brands": 1,
            "None of the above": 0
        }
    },
    {
        "q": "How often do you eat locally grown or seasonal produce?",
        "type": "single",
        "options": {
            "Always": 4,
            "Often": 3,
            "Sometimes": 2,
            "Rarely": 0
        }
    },
    {
        "q": "Do you use water-saving devices?",
        "type": "single",
        "options": {
            "Yes": 4,
            "Not sure": 2,
            "No": 0
        }
    },
    {
        "q": "Have you participated in environmental programs or clean-ups?",
        "type": "single",
        "options": {
            "Yes": 4,
            "No": 0
        }
    }
]

score = 0

with st.form("survey_form"):
    for idx, q in enumerate(questions):
        st.markdown(f"**{idx+1}. {q['q']}**")
        if q["type"] == "single":
            choice = st.radio("", list(q["options"].keys()), key=idx)
            score += q["options"][choice]
        elif q["type"] == "multi":
            choices = st.multiselect("", list(q["options"].keys()), key=idx)
            for c in choices:
                score += q["options"][c]
    submitted = st.form_submit_button("Submit")

if submitted:
    st.subheader(f"Your Sustainability Score: {score}")
    if score >= 30:
        st.success("🌟 Sustainability Star – keep leading the way!")
    elif score >= 20:
        st.info("🌿 On the Right Path – great work, keep improving!")
    else:
        st.warning("🌎 Room to Grow – start with small, daily changes!")
