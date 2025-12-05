import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
DATA_FILE = "students_data.csv"

def init_data_file():
    """
    Make sure students.csv exists.
    If not, create an empty file with the correct columns.
    """
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=[
            "id", "name", "age", "gender", "course", "marks", "attendance"
        ])
        df.to_csv(DATA_FILE, index=False)
def load_data():
    """Load CSV into a DataFrame."""
    init_data_file()
    return pd.read_csv(DATA_FILE)
def save_data(df: pd.DataFrame):
    """Save DataFrame back to CSV."""
    df.to_csv(DATA_FILE, index=False)
def generate_new_id(df: pd.DataFrame) -> int:
    """Generate next student ID."""
    if df.empty:
        return 1
    return int(df["id"].max()) + 1
def add_student():
    df = load_data()
    new_id = generate_new_id(df)

    print("\n--- Add New Student ---")
    name = input("Name        : ")
    age = int(input("Age         : "))
    gender = input("Gender (M/F): ")
    course = input("Course      : ")
    marks = float(input("Marks (0-100): "))
    attendance = float(input("Attendance % : "))

    new_row = {
        "id": new_id,
        "name": name,
        "age": age,
        "gender": gender,
        "course": course,
        "marks": marks,
        "attendance": attendance
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_data(df)
    print(f"\n Student added with ID: {new_id}\n")

def view_students():
    df = load_data()
    print("\n--- All Students ---")
    if df.empty:
        print("No records found.\n")
    else:
        print(df.to_string(index=False))
        print()

def search_student():
    df = load_data()
    if df.empty:
        print("\nNo records to search.\n")
        return

    print("\n--- Search Student ---")
    choice = input("Search by (1) ID or (2) Name? : ")

    if choice == "1":
        sid = int(input("Enter ID: "))
        result = df[df["id"] == sid]
    else:
        name = input("Enter name (part or full): ")
        result = df[df["name"].str.contains(name, case=False, na=False)]

    if result.empty:
        print("No matching student found.\n")
    else:
        print("\nResult:")
        print(result.to_string(index=False))
        print()

def update_student():
    df = load_data()
    if df.empty:
        print("\nNo records to update.\n")
        return

    view_students()
    sid = int(input("Enter ID of student to update: "))

    if sid not in df["id"].values:
        print("ID not found.\n")
        return

    idx = df.index[df["id"] == sid][0]
    print("\nLeave blank to keep old value.\n")

    name = input(f"Name ({df.at[idx, 'name']}): ") or df.at[idx, "name"]
    age_in = input(f"Age ({df.at[idx, 'age']}): ")
    age = int(age_in) if age_in else df.at[idx, "age"]

    gender = input(f"Gender ({df.at[idx, 'gender']}): ") or df.at[idx, "gender"]
    course = input(f"Course ({df.at[idx, 'course']}): ") or df.at[idx, "course"]

    marks_in = input(f"Marks ({df.at[idx, 'marks']}): ")
    marks = float(marks_in) if marks_in else df.at[idx, "marks"]

    att_in = input(f"Attendance ({df.at[idx, 'attendance']}): ")
    attendance = float(att_in) if att_in else df.at[idx, "attendance"]

    df.at[idx, "name"] = name
    df.at[idx, "age"] = age
    df.at[idx, "gender"] = gender
    df.at[idx, "course"] = course
    df.at[idx, "marks"] = marks
    df.at[idx, "attendance"] = attendance

    save_data(df)
    print("\nStudent updated.\n")


def delete_student():
    df = load_data()
    if df.empty:
        print("\nNo records to delete.\n")
        return

    view_students()
    sid = int(input("Enter ID of student to delete: "))

    if sid not in df["id"].values:
        print("ID not found.\n")
        return

    df = df[df["id"] != sid]
    save_data(df)
    print("\nStudent deleted.\n")

def show_statistics():
    df = load_data()
    if df.empty:
        print("\nNo data for statistics.\n")
        return

    print("\n--- Basic Statistics ---")
    print("Total students        :", len(df))
    print("Average marks         :", round(df["marks"].mean(), 2))
    print("Highest marks         :", df["marks"].max())
    print("Lowest marks          :", df["marks"].min())
    print("Average attendance    :", round(df["attendance"].mean(), 2))
    print()
    print("Top scorer            :", df.loc[df["marks"].idxmax(), "name"])
    print("Lowest scorer         :", df.loc[df["marks"].idxmin(), "name"])
    print("Course-wise avg marks :")
    print(df.groupby("course")["marks"].mean().round(2))
    print()

def show_top_students(n=5):
    df = load_data()
    if df.empty:
        print("\nNo data available.\n")
        return
    print(f"\n--- Top {n} Students by Marks ---")
    top = df.sort_values(by="marks", ascending=False).head(n)
    print(top[["id", "name", "course", "marks", "attendance"]].to_string(index=False))
    print()

def show_course_wise_average():
    df = load_data()
    if df.empty:
        print("\nNo data available.\n")
        return

    print("\n--- Average Marks by Course ---")
    course_avg = df.groupby("course")["marks"].mean().round(2).reset_index()
    print(course_avg.to_string(index=False))
    print()

def plot_marks_distribution():
    df = load_data()
    if df.empty:
        print("\nNo data to plot.\n")
        return

    sns.histplot(df["marks"], kde=True)
    plt.title("Marks Distribution")
    plt.xlabel("Marks")
    plt.ylabel("Count")
    plt.show()

def plot_attendance_distribution():
    df = load_data()
    if df.empty:
        print("\nNo data to plot.\n")
        return

    sns.histplot(df["attendance"], kde=True)
    plt.title("Attendance Percentage Distribution")
    plt.xlabel("Attendance %")
    plt.ylabel("Count")
    plt.show()

def plot_marks_vs_attendance():
    df = load_data()
    if df.empty:
        print("\nNo data to plot.\n")
        return

    sns.scatterplot(x="attendance", y="marks", hue="course", data=df)
    plt.title("Marks vs Attendance")
    plt.xlabel("Attendance %")
    plt.ylabel("Marks")
    plt.show()

def plot_course_average():
    df = load_data()
    if df.empty:
        print("\nNo data to plot.\n")
        return

    course_avg = df.groupby("course")["marks"].mean().reset_index()
    sns.barplot(x="course", y="marks", data=course_avg)
    plt.title("Average Marks by Course")
    plt.xlabel("Course")
    plt.ylabel("Average Marks")
    plt.show()

def plot_correlation_heatmap():
    df = load_data()
    if df.empty:
        print("\nNo data to plot.\n")
        return

    corr = df[["age", "marks", "attendance"]].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.show()

def main_menu():
    while True:
        print("\n===== Student Management System =====")
        print("1. Add student")
        print("2. View all students")
        print("3. Search student")
        print("4. Update student")
        print("5. Delete student")
        print("6. Show statistics")
        print("7. Show top 5 students")
        print("8. Show average marks by course")
        print("9. Plot marks distribution")
        print("10. Plot attendance distribution")
        print("11. Plot marks vs attendance")
        print("12. Plot course-wise average marks")
        print("13. Plot correlation heatmap")
        print("14. Exit")

        choice = input("Enter choice (1-14): ")

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            show_statistics()
        elif choice == "7":
            show_top_students()
        elif choice == "8":
            show_course_wise_average()
        elif choice == "9":
            plot_marks_distribution()
        elif choice == "10":
            plot_attendance_distribution()
        elif choice == "11":
            plot_marks_vs_attendance()
        elif choice == "12":
            plot_course_average()
        elif choice == "13":
            plot_correlation_heatmap()
        elif choice == "14":
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Try again.")
if __name__ == "__main__":
    main_menu()