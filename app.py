import streamlit as pd
import streamlit as st
import datetime
import pandas as pd

# பக்கத்தின் தலைப்பு மற்றும் வடிவமைப்பு
st.set_page_config(page_title="Lab Management System", layout="wide")
st.title("🩸 ரத்தப் பரிசோதனை நிலைய மேலாண்மை")

# பக்கவாட்டு மெனு (Sidebar Navigation)
menu = ["நோயாளி பதிவு (Registration)", "பரிசோதனை முடிவுகள் (Test Results)", "பதிவுகள் (View Records)"]
choice = st.sidebar.selectbox("மெனுவைத் தேர்ந்தெடுக்கவும்", menu)

# தற்காலிகமாக தரவைச் சேமிக்க (Session State)
if "patients" not in st.session_state:
    st.session_state.patients = []

# 1. நோயாளி பதிவுப் பக்கம்
if choice == "நோயாளி பதிவு (Registration)":
    st.header("👤 புதிய நோயாளி பதிவு மற்றும் பில்லிங்")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("நோயாளி பெயர் (Patient Name)")
        age = st.number_input("வயது (Age)", min_value=1, max_value=120, value=30)
        gender = st.radio("பாலினம் (Gender)", ["ஆண்", "பெண்", "இதர"])
        phone = st.text_input("மொபைல் எண் (Mobile No)")
    
    with col2:
        date = st.date_input("தேதி (Date)", datetime.date.today())
        doctor = st.text_input("பரிந்துரைத்த மருத்துவர் (Referred By)")
        tests = st.multiselect("பரிசோதனைகள் (Select Tests)", 
                               ["CBC (Rs. 300)", "Fastering Blood Sugar (Rs. 100)", "Thyroid Profile (Rs. 500)", "Lipid Profile (Rs. 600)"])
    
    if st.button("பதிவு செய் & பில் உருவாக்கு"):
        if name and phone and tests:
            patient_id = len(st.session_state.patients) + 1
            new_patient = {
                "ID": patient_id, "தேதி": date, "பெயர்": name, "வயது": age, 
                "பாலினம்": gender, "மொபைல்": phone, "மருத்துவர்": doctor, 
                "பரிசோதனைகள்": ", ".join(tests), "முடிவுகள்": "Pending"
            }
            st.session_state.patients.append(new_patient)
            st.success(f"🎉 நோயாளி வெற்றிகரமாகப் பதிவு செய்யப்பட்டார்! ID: {patient_id}")
        else:
            st.error("⚠️ தயவுசெய்து அனைத்து விபரங்களையும் பூர்த்தி செய்யவும்!")

# 2. பரிசோதனை முடிவுகள் பக்கம்
elif choice == "பரிசோதனை முடிவுகள் (Test Results)":
    st.header("📝 பரிசோதனை முடிவுகள் உள்ளீடு")
    
    if not st.session_state.patients:
        st.warning("தற்போது நோயாளிகள் யாரும் பதிவு செய்யப்படவில்லை.")
    else:
        patient_list = [f"{p['ID']} - {p['பெயர்']}" for p in st.session_state.patients]
        selected_p = st.selectbox("பரிசோதனை முடிவை உள்ளிட நோயாளியைத் தேர்ந்தெடுக்கவும்", patient_list)
        p_id = int(selected_p.split(" - ")[0])
        
        # தேர்ந்தெடுக்கப்பட்ட நோயாளியின் விபரங்களை எடுத்தல்
        for p in st.session_state.patients:
            if p["ID"] == p_id:
                st.write(f"**நோயாளி பெயர்:** {p['பெயர்']} | **பரிசோதனைகள்:** {p['பரிசோதனைகள்']}")
                results = st.text_area("பரிசோதனை முடிவுகளை உள்ளிடவும் (எ.கா: Hemoglobin: 14 g/dL, Sugar: 110 mg/dL)")
                
                if st.button("முடிவுகளைச் சேமிக்கவும்"):
                    p["முடிவுகள்"] = results
                    st.success("✅ பரிசோதனை முடிவுகள் வெற்றிகரமாகச் சேமிக்கப்பட்டன!")

# 3. பதிவுகள் பக்கம்
elif choice == "பதிவுகள் (View Records)":
    st.header("📊 லேப் பதிவுகள்")
    if st.session_state.patients:
        df = pd.DataFrame(st.session_state.patients)
        st.dataframe(df)
    else:
        st.info("காண்பிப்பதற்கு எந்தப் பதிவுகளும் இல்லை.")
