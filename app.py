import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Telecom Churn Prediction",
    page_icon="📊",
    layout="wide"
)

# ---------------- LOAD MODEL ---------------- #

model = pickle.load(open('randomforest.pkl', 'rb'))

# ---------------- SESSION STATE ---------------- #

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- AUTHENTICATION SYSTEM ---------------- #

if "users" not in st.session_state:

    st.session_state.users = {
        "admin": {
            "password": "admin123",
            "role": "Admin"
        }
    }

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""

if "username" not in st.session_state:
    st.session_state.username = ""

# ---------------- LOGIN / SIGNUP PAGE ---------------- #

if not st.session_state.logged_in:

    st.title("🔐 Telecom Churn Prediction System")

    st.markdown("""
    Welcome to the Telecom Customer Churn Prediction Dashboard
    """)

    menu = st.selectbox(
        "Select Option",
        [
            "User Sign In",
            "Admin Sign In",
            "Sign Up"
        ]
    )

    # ---------------- USER LOGIN ---------------- #

    if menu == "User Sign In":

        st.subheader("👤 User Login")

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login as User"):

            if username in st.session_state.users:

                user = st.session_state.users[username]

                if (
                    user["password"] == password
                    and user["role"] == "User"
                ):

                    st.session_state.logged_in = True
                    st.session_state.role = "User"
                    st.session_state.username = username

                    st.success("✅ User Login Successful")

                    st.rerun()

                else:
                    st.error("❌ Invalid User Credentials")

            else:
                st.error("❌ User Not Found")

    # ---------------- ADMIN LOGIN ---------------- #

    elif menu == "Admin Sign In":

        st.subheader("🛠 Admin Login")

        username = st.text_input("Admin Username")

        password = st.text_input(
            "Admin Password",
            type="password"
        )

        if st.button("Login as Admin"):

            if username in st.session_state.users:

                user = st.session_state.users[username]

                if (
                    user["password"] == password
                    and user["role"] == "Admin"
                ):

                    st.session_state.logged_in = True
                    st.session_state.role = "Admin"
                    st.session_state.username = username

                    st.success("✅ Admin Login Successful")

                    st.rerun()

                else:
                    st.error("❌ Invalid Admin Credentials")

            else:
                st.error("❌ Admin Not Found")

    # ---------------- SIGN UP ---------------- #

    elif menu == "Sign Up":

        st.subheader("📝 Create New Account")

        new_username = st.text_input(
            "Create Username"
        )

        new_password = st.text_input(
            "Create Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        if st.button("Create Account"):

            if new_username in st.session_state.users:

                st.warning("⚠ Username already exists")

            elif new_password != confirm_password:

                st.error("❌ Passwords do not match")

            elif len(new_password) < 4:

                st.warning(
                    "⚠ Password must be at least 4 characters"
                )

            else:

                st.session_state.users[new_username] = {
                    "password": new_password,
                    "role": "User"
                }

                st.success(
                    "✅ Account Created Successfully"
                )

                st.info(
                    "Now login using User Sign In"
                )

# ---------------- MAIN APPLICATION ---------------- #

else:

    # ---------------- FEATURE COLUMNS ---------------- #

    columns = [
        'tenure',
        'PhoneService',
        'Contract',
        'PaperlessBilling',
        'PaymentMethod',
        'MonthlyCharges'
    ]

    # ---------------- SIDEBAR ---------------- #

    st.sidebar.success(
        f"Logged in as: "
        f"{st.session_state.username}"
    )

    st.sidebar.info(
        f"Role: {st.session_state.role}"
    )

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.role = ""
        st.session_state.username = ""

        st.rerun()

    # ---------------- PREDICTION FUNCTION ---------------- #

    def predict_churn(input_data):

        input_df = pd.DataFrame(
            [input_data],
            columns=columns
        )

        prediction = model.predict(input_df)

        probability = model.predict_proba(
            input_df
        )[:, 1]

        return prediction[0], probability[0]

    # ---------------- TITLE ---------------- #

    st.title("📊 Telecom Churn Prediction Dashboard")

    st.markdown(f"""
    Welcome **{st.session_state.username}** 👋
    """)

    st.markdown("""
    Predict whether a telecom customer is likely
    to churn using Machine Learning.
    """)

    st.markdown("---")

    # ---------------- SIDEBAR INPUTS ---------------- #

    st.sidebar.title("📋 Customer Details")

    with st.sidebar.expander(
        "Enter Customer Information",
        expanded=True
    ):

        tenure = st.slider(
            "Tenure (months)",
            min_value=0,
            max_value=100,
            value=1
        )

        phone_service = st.selectbox(
            "Phone Service",
            [0, 1],
            format_func=lambda x:
            "Yes" if x == 1 else "No"
        )

        contract = st.selectbox(
            "Contract Type",
            [0, 1, 2],
            format_func=lambda x: {
                0: "Month-to-month",
                1: "One year",
                2: "Two year"
            }[x]
        )

        paperless_billing = st.selectbox(
            "Paperless Billing",
            [0, 1],
            format_func=lambda x:
            "Yes" if x == 1 else "No"
        )

        payment_method = st.selectbox(
            "Payment Method",
            [0, 1, 2, 3],
            format_func=lambda x: {
                0: "Bank Transfer",
                1: "Credit Card",
                2: "Electronic Check",
                3: "Mailed Check"
            }[x]
        )

        monthly_charges = st.number_input(
            "Monthly Charges",
            min_value=0.0,
            value=50.0
        )

    # ---------------- INPUT DATA ---------------- #

    input_data = {
        'tenure': tenure,
        'PhoneService': phone_service,
        'Contract': contract,
        'PaperlessBilling': paperless_billing,
        'PaymentMethod': payment_method,
        'MonthlyCharges': monthly_charges
    }

    # ---------------- PREDICT BUTTON ---------------- #

    if st.button("🚀 Predict Churn"):

        prediction, probability = predict_churn(
            input_data
        )

        # ---------------- RISK LEVEL ---------------- #

        if probability < 0.3:
            risk = "Low Risk"

        elif probability < 0.6:
            risk = "Medium Risk"

        else:
            risk = "High Risk"

        # ---------------- SAVE HISTORY ---------------- #

        st.session_state.history.append({
            "Tenure": tenure,
            "Monthly Charges": monthly_charges,
            "Probability": round(
                probability * 100,
                2
            ),
            "Risk": risk
        })

        # ---------------- RESULTS ---------------- #

        st.subheader("📈 Prediction Result")

        if risk == "Low Risk":
            st.success("🟢 Low Risk Customer")

        elif risk == "Medium Risk":
            st.warning("🟠 Medium Risk Customer")

        else:
            st.error("🔴 High Risk Customer")

        # ---------------- METRICS ---------------- #

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Churn Probability",
                f"{probability * 100:.2f}%"
            )

        with col2:

            st.metric(
                "Prediction",
                "Churn"
                if prediction == 1
                else "No Churn"
            )

        st.markdown("---")

        # ---------------- GAUGE CHART ---------------- #

        st.subheader(
            "📊 Churn Probability Gauge"
        )

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=probability * 100,
            title={
                'text': "Churn Probability"
            },
            gauge={
                'axis': {
                    'range': [0, 100]
                },
                'steps': [
                    {
                        'range': [0, 30],
                        'color': "lightgreen"
                    },
                    {
                        'range': [30, 60],
                        'color': "orange"
                    },
                    {
                        'range': [60, 100],
                        'color': "red"
                    }
                ]
            }
        ))

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ---------------- RETENTION SUGGESTIONS ---------------- #

        st.markdown("---")

        st.subheader("💡 Customer Retention Suggestions")

        if risk == "High Risk":

            st.error(
                "Customer requires immediate retention action."
            )

            st.markdown("""
            ### Recommended Actions

            - 🎁 Offer discount coupons
            - 📞 Customer support follow-up
            - 📦 Upgrade service plan
            - 💳 Flexible payment options
            - ⭐ Loyalty rewards program
            """)

        elif risk == "Medium Risk":

            st.warning(
                "Customer may require engagement strategies."
            )

            st.markdown("""
            ### Recommended Actions

            - 📧 Promotional offers
            - 🎯 Personalized recommendations
            - 📞 Feedback collection
            - 💰 Moderate discounts
            """)

        else:

            st.success(
                "Customer is stable and satisfied."
            )

            st.markdown("""
            ### Recommended Actions

            - 🌟 Continue good service
            - 🎉 Reward loyal customers
            - 📈 Offer premium plans
            """)

    # ---------------- ANALYTICS DASHBOARD ---------------- #

    if len(st.session_state.history) > 0:

        st.markdown("---")

        st.subheader("📊 Prediction Analytics Dashboard")

        history_df = pd.DataFrame(
            st.session_state.history
        )

        # ---------------- METRICS ---------------- #

        total_predictions = len(history_df)

        high_risk = len(
            history_df[
                history_df["Risk"] == "High Risk"
            ]
        )

        low_risk = len(
            history_df[
                history_df["Risk"] == "Low Risk"
            ]
        )

        avg_probability = history_df[
            "Probability"
        ].mean()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Predictions",
            total_predictions
        )

        col2.metric(
            "High Risk Customers",
            high_risk
        )

        col3.metric(
            "Low Risk Customers",
            low_risk
        )

        col4.metric(
            "Average Churn %",
            f"{avg_probability:.2f}%"
        )

        st.markdown("---")

        # ---------------- HISTORY TABLE ---------------- #

        st.subheader("📜 Recent Predictions")

        st.dataframe(history_df)

        # ---------------- CHARTS ---------------- #

        col1, col2 = st.columns(2)

        with col1:

            pie_chart = px.pie(
                history_df,
                names='Risk',
                title='Risk Distribution'
            )

            st.plotly_chart(
                pie_chart,
                use_container_width=True
            )

        with col2:

            risk_count = (
                history_df["Risk"]
                .value_counts()
                .reset_index()
            )

            risk_count.columns = [
                "Risk",
                "Count"
            ]

            bar_chart = px.bar(
                risk_count,
                x="Risk",
                y="Count",
                title="Customer Risk Analysis"
            )

            st.plotly_chart(
                bar_chart,
                use_container_width=True
            )

    # ---------------- ADMIN FEATURES ---------------- #

    if st.session_state.role == "Admin":

        st.markdown("---")

        st.subheader(
            "📁 Bulk Customer Churn Prediction"
        )

        uploaded_file = st.file_uploader(
            "Upload CSV File",
            type=["csv"]
        )

        if uploaded_file is not None:

            try:

                batch_df = pd.read_csv(
                    uploaded_file
                )

                st.write("### Uploaded Dataset")

                st.dataframe(
                    batch_df.head()
                )

                required_columns = columns

                if all(
                    col in batch_df.columns
                    for col in required_columns
                ):

                    predictions = model.predict(
                        batch_df
                    )

                    probabilities = (
                        model.predict_proba(
                            batch_df
                        )[:, 1]
                    )

                    batch_df["Prediction"] = [
                        "Churn"
                        if p == 1
                        else "No Churn"
                        for p in predictions
                    ]

                    batch_df[
                        "Churn Probability"
                    ] = (
                        probabilities * 100
                    ).round(2)

                    def get_risk(prob):

                        if prob < 30:
                            return "Low Risk"

                        elif prob < 60:
                            return "Medium Risk"

                        else:
                            return "High Risk"

                    batch_df[
                        "Risk Level"
                    ] = batch_df[
                        "Churn Probability"
                    ].apply(get_risk)

                    st.write(
                        "### Prediction Results"
                    )

                    st.dataframe(batch_df)

                    # ---------------- BAR CHART ---------------- #

                    st.subheader(
                        "📊 Bulk Prediction Analysis"
                    )

                    risk_count = (
                        batch_df["Risk Level"]
                        .value_counts()
                        .reset_index()
                    )

                    risk_count.columns = [
                        "Risk",
                        "Count"
                    ]

                    bar_chart = px.bar(
                        risk_count,
                        x="Risk",
                        y="Count",
                        title="Customer Risk Levels"
                    )

                    st.plotly_chart(
                        bar_chart,
                        use_container_width=True
                    )

                    # ---------------- DOWNLOAD ---------------- #

                    csv = batch_df.to_csv(
                        index=False
                    ).encode('utf-8')

                    st.download_button(
                        label="⬇ Download Prediction Results",
                        data=csv,
                        file_name='churn_predictions.csv',
                        mime='text/csv'
                    )

                else:

                    st.error(
                        f"CSV must contain columns: "
                        f"{required_columns}"
                    )

            except Exception as e:

                st.error(f"Error: {e}")

        # ---------------- MODEL INFO ---------------- #

        st.markdown("---")

        st.markdown("""
        ### 📌 Model Information

        - **Model Used:** Random Forest  
        - **Model Accuracy:** 84%  
        """)