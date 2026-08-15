import streamlit as st
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

from database import (
    create_database,
    register_user,
    login_user,
    add_student,
    get_students
)



# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="🎓",
    layout="wide"
)

create_database()
# ---------------- LOAD DATA ----------------

# ---------------- LOGIN SYSTEM ----------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "username" not in st.session_state:
    st.session_state.username = None


if not st.session_state.logged_in:

    st.title("🎓 Student Performance Prediction System")

    st.subheader("🔐 Login")

    login_username = st.text_input(
        "Username"
    )

    login_password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        user = login_user(
            login_username,
            login_password
        )

        if user:

            st.session_state.logged_in = True
            st.session_state.user_id = user[0]
            st.session_state.username = user[1]

            st.success("✅ Login successful!")

            st.rerun()

        else:

            st.error(
                "❌ Invalid username or password."
            )

    st.divider()

    st.subheader("📝 New User?")

    register_username = st.text_input(
        "Create Username"
    )

    register_password = st.text_input(
        "Create Password",
        type="password"
    )

    if st.button("Register"):

        if (
            register_username.strip() == ""
            or register_password.strip() == ""
        ):

            st.warning(
                "Please enter username and password."
            )

        else:

            created = register_user(
                register_username,
                register_password
            )

            if created:

                st.success(
                    "✅ Account created successfully! "
                    "You can now login."
                )

            else:

                st.error(
                    "❌ Username already exists."
                )

    st.stop()





    if st.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None

        st.rerun()
        
st.sidebar.success(
    f"👋 Welcome, {st.session_state.username}"
)
data = pd.read_csv("student_data.csv")

encoder = LabelEncoder()
data["performance"] = encoder.fit_transform(data["performance"])

X = data.drop("performance", axis=1)
y = data["performance"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ---------------- MACHINE LEARNING MODEL ----------------

model = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(
        max_iter=1000,
        random_state=42
    ))
])

model.fit(X_train, y_train)

# Model accuracy
accuracy = model.score(X_test, y_test)

# ---------------- TITLE ----------------

st.title("🎓 AI-Driven Student Performance Prediction System")

st.write(
    "An intelligent machine learning system for predicting student academic performance."
)

st.divider()

# ---------------- DASHBOARD ----------------

st.subheader("📊 Performance Dashboard")

# Get only the logged-in user's student records
dashboard_data = get_students(
    st.session_state.user_id
)

total_students = len(dashboard_data)

good_students = len(
    dashboard_data[
        dashboard_data["Prediction"] == "Good"
    ]
)

average_students = len(
    dashboard_data[
        dashboard_data["Prediction"] == "Average"
    ]
)

at_risk_students = len(
    dashboard_data[
        dashboard_data["Prediction"] == "At Risk"
    ]
)
col1, col2, col3, col4 = st.columns(4)

col1.metric("👨‍🎓 Total Students", total_students)
col2.metric("🟢 Good", good_students)
col3.metric("🟡 Average", average_students)
col4.metric("🔴 At Risk", at_risk_students)

st.divider()


# ---------------- SIDEBAR INPUT ----------------

st.sidebar.header("👨‍🎓 Student Details")

with st.sidebar.form("student_form"):

    student_name = st.text_input(
        "Student Name"
    )

    student_id = st.text_input(
        "Student ID"
    )

    attendance = st.slider(
        "Attendance (%)",
        0,
        100,
        75
    )

    internal_marks = st.slider(
        "Internal Marks",
        0,
        100,
        60
    )

    assignment_marks = st.slider(
        "Assignment Marks",
        0,
        100,
        65
    )

    study_hours = st.slider(
        "Study Hours per Day",
        0,
        12,
        3
    )

    previous_marks = st.slider(
        "Previous Marks",
        0,
        100,
        60
    )

    predict_button = st.form_submit_button(
        "🔮 Predict Performance"
    )

# ---------------- MAIN AREA ----------------

if predict_button:

    if student_name.strip() == "" or student_id.strip() == "":
        st.warning(
            "Please enter both Student Name and Student ID."
        )

    else:

        # ---------------- STUDENT DATA ----------------

        student = pd.DataFrame({
        "attendance": [attendance],
        "internal_marks": [internal_marks],
        "assignment_marks": [assignment_marks],
        "study_hours": [study_hours],
        "previous_marks": [previous_marks]

        })
        

        # ---------------- PERFORMANCE SCORE ----------------

        study_score = min(study_hours * 10, 100)

        performance_score = (
            attendance * 0.20
            + internal_marks * 0.25
            + assignment_marks * 0.20
            + study_score * 0.15
            + previous_marks * 0.20
        )

        # ---------------- FINAL PREDICTION ----------------

        if performance_score >= 72:
            result = "Good"

        elif performance_score >= 52:
            result = "Average"

        else:
            result = "At Risk"

        # ---------------- RESULT ----------------

        st.subheader("🔮 Prediction Result")

        st.write(
            f"### Student: {student_name}"
        )

        st.write(
            f"**Student ID:** {student_id}"
        )

        if result == "Good":

            st.success(
                "🎉 Performance Prediction: GOOD"
            )

        elif result == "Average":

            st.warning(
                "📚 Performance Prediction: AVERAGE"
            )

        else:

            st.error(
                "⚠️ Performance Prediction: AT RISK"
            )

        # ---------------- PERFORMANCE SCORE ----------------

        st.metric(
            "📊 Overall Performance Score",
            f"{performance_score:.1f} / 100"
        )

        st.progress(
            int(performance_score) / 100
        )

        # ---------------- RECOMMENDATION ----------------

        st.subheader("💡 Recommendation")

        if result == "Good":

            st.write(
                "Excellent performance. Continue maintaining "
                "good attendance, study habits and academic performance."
            )

        elif result == "Average":

            st.write(
                "The student should increase study hours and "
                "focus on improving internal and assignment marks."
            )

        else:

            st.write(
                "The student should improve attendance, study "
                "hours, assignments and academic performance."
            )

        # ---------------- CHART ----------------

        st.subheader("📊 Student Performance Analysis")

        analysis_data = pd.DataFrame({
            "Parameter": [
                "Attendance",
                "Internal Marks",
                "Assignment Marks",
                "Study Hours",
                "Previous Marks"
            ],

            "Value": [
                attendance,
                internal_marks,
                assignment_marks,
                study_hours,
                previous_marks
            ]
        })

        st.bar_chart(
            analysis_data.set_index("Parameter")
        )

        # ---------------- SAVE RECORD ----------------

        add_student(
            st.session_state.user_id,
            student_name,
            student_id,
            attendance,
            internal_marks,
            assignment_marks,
            study_hours,
            previous_marks,
            result,
            performance_score
        )

        st.success(
            "✅ Prediction saved successfully!"
        )





# ---------------- SAVED RECORDS ----------------
st.divider()

st.subheader("📋 Saved Student Records")

records = get_students(
    st.session_state.user_id
)

if len(records) > 0:

    st.dataframe(
        records,
        use_container_width=True
    )

else:

    st.info(
        "No student records available yet."
    )

# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "AI-Driven Student Performance Prediction System | "
    "Python + Machine Learning"
)