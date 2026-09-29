import streamlit as st
import pandas as pd
import pickle
from PIL import Image
from user_auth import authenticate_user, register_user

# ✅ Set page config FIRST
st.set_page_config(page_title="Credit Card Fraud Detection", layout="centered")

# ✅ Try loading logo
try:
    logo = Image.open("logo.png")
    st.image(logo, use_container_width=True)  # ✅ updated here
except FileNotFoundError:
    st.title("💳 Credit Card Fraud Detection")

# ✅ Load trained model
with open("fraud_model.pkl", "rb") as f:
    model = pickle.load(f)

# Sidebar for login/signup/logout
st.sidebar.title("🔐 User Access")
auth_mode = st.sidebar.radio("Choose Action", ["Login", "Sign Up"])

# ✅ Handle login
if auth_mode == "Login":
    st.sidebar.subheader("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    login_button = st.sidebar.button("Login")

    if login_button:
        if authenticate_user(username, password):
            st.session_state["user"] = username
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid username or password.")

# ✅ Handle sign up
elif auth_mode == "Sign Up":
    st.sidebar.subheader("Create Account")
    new_username = st.sidebar.text_input("New Username")
    new_password = st.sidebar.text_input("New Password", type="password")
    email = st.sidebar.text_input("Email")
    signup_button = st.sidebar.button("Register")

    if signup_button:
        if register_user(new_username, new_password, email):
            st.success("✅ Account created successfully! Please log in.")
        else:
            st.warning("⚠️ Username already exists. Try a different one.")

# ✅ Main section (only for logged in users)
if "user" in st.session_state:
    st.header("📊 Upload Credit Card Transactions")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("### 🔍 Preview of Uploaded Data")
        st.dataframe(df.head())

        if "IsFraud" in df.columns:
            frauds = df[df["IsFraud"] == 1]
            if not frauds.empty:
                st.error("⚠️ Actual Fraudulent Transactions Detected")
                st.dataframe(frauds)
                st.download_button("Download Fraud Transactions", frauds.to_csv(index=False), file_name="frauds_detected.csv")
            else:
                st.success("✅ No fraud in uploaded data.")
        else:
            try:
                X = df.drop(columns=["TransactionID"], errors="ignore")
                preds = model.predict(X)
                df["Prediction"] = preds
                predicted_frauds = df[df["Prediction"] == 1]

                if not predicted_frauds.empty:
                    st.warning("⚠️ Fraudulent Transactions Predicted!")
                    st.dataframe(predicted_frauds)
                    st.download_button("Download Predicted Frauds", predicted_frauds.to_csv(index=False), file_name="fraud_predictions.csv")
                else:
                    st.success("✅ No fraud predicted.")
            except Exception as e:
                st.error(f"Error during prediction: {e}")

    # ✅ Add logout button
    if st.sidebar.button("Logout"):
        del st.session_state["user"]
        st.success("Logged out successfully!")
        st.rerun()

else:
    st.info("🔐 Please log in or sign up to access fraud detection.")
