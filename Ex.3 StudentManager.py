import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk
import os

# Create main window
main = tk.Tk()
main.title("Student Manager") # Title of the window
main.geometry("800x600")  # Size of the window
main.config(bg="#4a4e69") # Background color

# Function to read student data from the file
def read_student_data(file_path):  # Function to read student data from the file
    students = [] 
    with open(r"C:\Users\Hp\OneDrive\Desktop\AP.Assessment1\studentMarks.txt") as file:  # Path to the file
        lines = file.readlines()   # Read all lines from the file
        num_students = int(lines[0].strip())   # Number of students
        for line in lines[1:num_students + 1]:   # Loop through each line
            parts = line.strip().split(',')    # Split the line into parts
            # Check if there are enough parts in the line
            if len(parts) < 6:    # If there are not enough parts, skip the line
                print(f"Skipping invalid line: {line}")   # Print a message
                continue
            student_code = int(parts[0])    # Student code
            name = parts[1]     # Student name
            marks = list(map(int, parts[2:5]))   # Marks
            exam_mark = int(parts[5])     # Exam mark
            total_coursework = sum(marks)    # Total coursework mark
            overall_percentage = (total_coursework + exam_mark) / 160 * 100     # Overall percentage
            grade = assign_grade(overall_percentage)      # Assign grade
            students.append({    # Append a dictionary to the list
                'code': student_code,
                'name': name,
                'total_coursework': total_coursework,
                'exam_mark': exam_mark,
                'overall_percentage': overall_percentage,
                'grade': grade
            })
    return students

# Function to save student data back to the file
def save_student_data(file_path):   # Function to save student data back to the file
    with open(file_path, 'w') as file:    # Open the file in write mode
        file.write(f"{len(students)}\n")    # Write the number of students
        for student in students:     # Loop through each student
             # Write the data with each coursework mark as a separate value
            coursework_marks = ','.join(map(str, [student['total_coursework'] // 3] * 3))  # Assuming equal coursework marks
            file.write(f"{student['code']},{student['name']},{coursework_marks},{student['exam_mark']}\n")    # Write the line

# Function to display all student records
def view_all_students(): 
    output = "" 
    total_percentage = 0 
    num_students = len(students)
    for student in students:
        output += f"Name: {student['name']}\n"
        output += f"Student Number: {student['code']}\n"
        output += f"Total Coursework Mark: {student['total_coursework']}\n"
        output += f"Exam Mark: {student['exam_mark']}\n"
        output += f"Overall Percentage: {student['overall_percentage']:.2f}%\n"
        output += f"Grade: {student['grade']}\n\n"
        total_percentage += student['overall_percentage']

    #  Calculate the average percentage
    avg_percentage = total_percentage / num_students if num_students else 0
    output += f"Total Students: {num_students}\n"
    output += f"Average Percentage: {avg_percentage:.2f}%\n"
    
    txt_area.delete(1.0, tk.END)  # Clear previous text
    txt_area.insert(tk.END, output)  # Insert new output

# Function to view individual student record
def view_individual_student(): 
    selected_student = combobox.get()   # Get the selected student code
    for student in students:      # Loop through each student
        if f"{student['name']}" in selected_student: 
            output = (
                f"Name: {student['name']}\n"
                f"Student Number: {student['code']}\n"
                f"Total Coursework Mark: {student['total_coursework']}\n"
                f"Exam Mark: {student['exam_mark']}\n"
                f"Overall Percentage: {student['overall_percentage']:.2f}%\n"
                f"Grade: {student['grade']}"
            )
            txt_area.delete(1.0, tk.END)  # Clear previous text
            txt_area.insert(tk.END, output)  # Insert new output
            return
    messagebox.showerror("Error", "Student not found.")

# Function to show student with highest total score
def show_highest_student():
    if students:
        highest_student = max(students, key=lambda s: s['total_coursework'] + s['exam_mark'])
        output = (
            f"Name: {highest_student['name']}\n"
            f"Student Number: {highest_student['code']}\n"
            f"Total Coursework Mark: {highest_student['total_coursework']}\n"
            f"Exam Mark: {highest_student['exam_mark']}\n"
            f"Overall Percentage: {highest_student['overall_percentage']:.2f}%\n"
            f"Grade: {highest_student['grade']}"
        )
        txt_area.delete(1.0, tk.END)  # Clear previous text
        txt_area.insert(tk.END, output)  # Insert new output
    else:
        messagebox.showinfo("Info", "No student records available.")

# Function to show student with lowest total score
def show_lowest_student():
    if students:
        lowest_student = min(students, key=lambda s: s['total_coursework'] + s['exam_mark'])
        output = (
            f"Name: {lowest_student['name']}\n"
            f"Student Number: {lowest_student['code']}\n"
            f"Total Coursework Mark: {lowest_student['total_coursework']}\n"
            f"Exam Mark: {lowest_student['exam_mark']}\n"
            f"Overall Percentage: {lowest_student['overall_percentage']:.2f}%\n"
            f"Grade: {lowest_student['grade']}"
        )
        txt_area.delete(1.0, tk.END)  # Clear previous text
        txt_area.insert(tk.END, output)  # Insert new output
    else:
        messagebox.showinfo("Info", "No student records available.")

# Function to assign grade based on percentage
def assign_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 70:
        return 'A'
    elif percentage >= 60:
        return 'B'
    elif percentage >= 50:
        return 'C'
    elif percentage >= 40:
        return 'D'
    else:
        return 'F'
    

# Function to sort students
def sort_students(order):
    global students
    if order == "Descending":   # Sort in descending order

        students.sort(key=lambda s: s['overall_percentage'])
    else:
        students.sort(key=lambda s: s['overall_percentage'], reverse=True)
    view_all_students()  # Refresh the display after sorting

# Function to add a student record
def add_student():
    def save_new_student():
        try:
            student_code = int(entry_code.get())
            name = entry_name.get()
            total_coursework = int(entry_coursework.get())
            exam_mark = int(entry_exam.get())
            overall_percentage = (total_coursework + exam_mark) / 160 * 100
            grade = assign_grade(overall_percentage)
            new_student = {
                'code': student_code,
                'name': name,
                'total_coursework': total_coursework,
                'exam_mark': exam_mark,
                'overall_percentage': overall_percentage,
                'grade': grade
            }
            students.append(new_student)
            save_student_data(file_path)  # Save to file
            messagebox.showinfo("Success", "Student record added successfully.")
            add_window.destroy()
            view_all_students()  # Refresh the display
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numeric values for code, coursework, and exam.")
        update_combobox()

    # Create a new window for adding student
    add_window = tk.Toplevel(main)
    add_window.title("Add Student")
    add_window.geometry("400x300")
    add_window.config(bg="#4a4e69")


    # Labels and entry fields for new student
    tk.Label(add_window, text="Student Code:", bg="#4a4e69", fg="#ffffff").pack(pady=5)
    entry_code = tk.Entry(add_window)
    entry_code.pack(pady=5)

    tk.Label(add_window, text="Name:", bg="#4a4e69", fg="#ffffff").pack(pady=5)
    entry_name = tk.Entry(add_window)
    entry_name.pack(pady=5)

    tk.Label(add_window, text="Total Coursework Mark:", bg="#4a4e69", fg="#ffffff").pack(pady=5)
    entry_coursework = tk.Entry(add_window)
    entry_coursework.pack(pady=5)

    tk.Label(add_window, text="Exam Mark:", bg="#4a4e69", fg="#ffffff").pack(pady=5)
    entry_exam = tk.Entry(add_window)
    entry_exam.pack(pady=5)

    # Button to save new student
    tk.Button(add_window, text="Add Student", command=save_new_student).pack(pady=10)

# Function to delete a student record
def delete_student():
    selected_student = combobox.get()
    for student in students:
        if f"{student['name']}" in selected_student:
            students.remove(student)
            save_student_data(file_path)  # Save to file
            messagebox.showinfo("Success", "Student record deleted successfully.")
            view_all_students()  # Refresh the display
            return
    messagebox.showerror("Error", "Student not found.")
    update_combobox()

# Function to update a student record
def update_student():
    selected_student = combobox.get()
    for student in students:
        if f"{student['name']}" in selected_student:
            def save_updated_student():
                try:
                    student_code = int(entry_code.get())
                    name = entry_name.get()
                    total_coursework = int(entry_coursework.get())
                    exam_mark = int(entry_exam.get())
                    overall_percentage = (total_coursework + exam_mark) / 160 * 100
                    grade = assign_grade(overall_percentage)

                    student['code'] = student_code
                    student['name'] = name
                    student['total_coursework'] = total_coursework
                    student['exam_mark'] = exam_mark
                    student['overall_percentage'] = overall_percentage
                    student['grade'] = grade

                    save_student_data(file_path)  # Save to file
                    messagebox.showinfo("Success", "Student record updated successfully.")
                    update_window.destroy()
                    view_all_students()  # Refresh the display
                except ValueError:
                    messagebox.showerror("Error", "Invalid input. Please enter numeric values.")

            # Create a new window for updating student
            update_window = tk.Toplevel(main)   # Create a new window
            update_window.title("Update Student")   # Set the title of the window
            update_window.geometry("400x300")   # Set the size of the window
            update_window.config(bg="#4a4e69")    # Set the background color of the window


            # Populate current values
            entry_code = tk.Entry(update_window) 
            entry_code.insert(0, student['code'])
            entry_name = tk.Entry(update_window)
            entry_name.insert(0, student['name'])
            entry_coursework = tk.Entry(update_window)
            entry_coursework.insert(0, student['total_coursework'])
            entry_exam = tk.Entry(update_window)
            entry_exam.insert(0, student['exam_mark'])

            # Labels and entry fields for updating student
            tk.Label(update_window, text="Student Code:", bg="#4a4e69", fg="#ffffff").pack(pady=5)
            entry_code.pack(pady=5)

            tk.Label(update_window, text="Name:", bg="#4a4e69", fg="#ffffff").pack(pady=5)
            entry_name.pack(pady=5)

            tk.Label(update_window, text="Total Coursework Mark:", bg="#4a4e69", fg="#ffffff").pack(pady=5)
            entry_coursework.pack(pady=5)

            tk.Label(update_window, text="Exam Mark:", bg="#4a4e69", fg="#ffffff").pack(pady=5)
            entry_exam.pack(pady=5)

            # Button to save updated student
            tk.Button(update_window, text="Update Student", command=save_updated_student).pack(pady=10)
            return
    messagebox.showerror("Error", "Student not found.")

# Load the student data from the file
students = []
file_path =( r"C:\Users\Hp\OneDrive\Desktop\AP.Assessment1\studentMarks.txt")  # Adjust this path as necessary
if os.path.exists(file_path):
    students = read_student_data(file_path)
else:
    messagebox.showerror("Error", "Student data file not found.")

# Create a frame for the buttons above the text area
button_frame = tk.Frame(main, bg="#4a4e69")
button_frame.pack(pady=10)

# Define button styles
button_style = {
    'bg': '#00a8cc',  # Light blue background
    'fg': '#ffffff',  # White text
    'font': ('Arial', 12, 'bold'),
    'padx': 10,
    'pady': 5,
}

# Menu buttons in the button frame
btn_view_all = tk.Button(button_frame, text="View All Students", command=view_all_students, **button_style)
btn_view_all.grid(row=0 , column=0, padx=5, pady=5)


btn_highest = tk.Button(button_frame, text="Highest Scoring Student", command=show_highest_student, **button_style)
btn_highest.grid(row=0 , column=1, padx=5, pady=5)


btn_lowest = tk.Button(button_frame, text="Lowest Scoring Student", command=show_lowest_student, **button_style)
btn_lowest.grid(row=0, column=2, padx=5, pady=5)

btn_sort = tk.Button(button_frame, text="Sort Students", command=lambda: sort_students("Ascending"), **button_style)
btn_sort.grid(row=0, column=3, padx=5, pady=5)

btn_add = tk.Button(button_frame, text="Add Student", command=add_student, **button_style)
btn_add.grid(row=1, column=0, padx=5, pady=5)

btn_delete = tk.Button(button_frame, text="Delete Student", command=delete_student, **button_style)
btn_delete.grid(row=1, column=1, padx=5, pady=5)

btn_update = tk.Button(button_frame, text="Update Student", command=update_student, **button_style)
btn_update.grid(row=1, column=2, padx=5, pady=5)

# Create text area for displaying output
txt_area = scrolledtext.ScrolledText(main, width=60, height=20, bg="#f0f0f0", fg="#333", font=("Arial", 12))
txt_area.pack(pady=10)

# Create a frame for viewing individual student records
individual_frame = tk.Frame(main, bg="#4a4e69")
individual_frame.pack(pady=5)

# Label for individual student view
label_individual = tk.Label(individual_frame, text="View Individual Student:", bg="#4a4e69", fg="#ffffff", font=("Arial", 12))
label_individual.pack(side=tk.LEFT, padx=(0, 5))

combobox = None
# Function to update the combobox values with the current student names
def update_combobox():
    combobox['values'] = [f"{student['name']}" for student in students]
    combobox.set("Select a student")  # Reset to default text

# Combobox for selecting a student
combobox = ttk.Combobox(individual_frame, width=40, font=("Arial", 12))
combobox['values'] = [f"{student['name']}" for student in students]  # Populate with student names
combobox.pack(side=tk.LEFT, padx=(0, 5))
combobox.set("Select a student")  # Set a default value

# Button for viewing individual student record from combobox
btn_view_individual = tk.Button(individual_frame, text="View Selected Student", command=view_individual_student, **button_style)
btn_view_individual.pack(side=tk.LEFT)

main.mainloop()
