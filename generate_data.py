import pandas as pd
import random

students = []

# Generate a large pool of realistic student data
for i in range(3000):

    attendance = random.randint(40, 100)
    internal_marks = random.randint(30, 100)
    assignment_marks = random.randint(30, 100)
    study_hours = random.randint(1, 10)
    previous_marks = random.randint(30, 100)

    # Convert study hours to a score
    study_score = study_hours * 10

    # Calculate overall performance score
    score = (
        attendance * 0.20
        + internal_marks * 0.25
        + assignment_marks * 0.20
        + study_score * 0.15
        + previous_marks * 0.20
    )

    # Add some natural variation
    score += random.uniform(-8, 8)

    if score >= 72:
        performance = "Good"

    elif score >= 52:
        performance = "Average"

    else:
        performance = "At Risk"

    students.append({
        "attendance": attendance,
        "internal_marks": internal_marks,
        "assignment_marks": assignment_marks,
        "study_hours": study_hours,
        "previous_marks": previous_marks,
        "performance": performance
    })


data = pd.DataFrame(students)

# Balance the three categories
good = data[data["performance"] == "Good"].sample(
    n=500,
    random_state=42
)

average = data[data["performance"] == "Average"].sample(
    n=500,
    random_state=42
)

at_risk = data[data["performance"] == "At Risk"].sample(
    n=500,
    random_state=42
)

# Combine the balanced data
data = pd.concat(
    [good, average, at_risk],
    ignore_index=True
)

# Shuffle
data = data.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

# Save
data.to_csv(
    "student_data.csv",
    index=False
)

print("✅ Realistic balanced dataset created!")
print("Total records:", len(data))
print("\nPerformance distribution:")
print(data["performance"].value_counts())