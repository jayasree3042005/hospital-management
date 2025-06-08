import sqlite3
from tkinter import *
from tkinter import messagebox

# Database Setup
conn = sqlite3.connect(r"patient.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    age INTEGER,
                    disease TEXT,
                    contact TEXT)''')
conn.commit()

# Functions
def add_patient():
    name = entry_name.get()
    age = entry_age.get()
    disease = entry_disease.get()
    contact = entry_contact.get()

    if name and age and disease and contact:
        cursor.execute("INSERT INTO patients (name, age, disease, contact) VALUES (?, ?, ?, ?)", (name, age, disease, contact))
        conn.commit()
        entry_name.delete(0, END)
        entry_age.delete(0, END)
        entry_disease.delete(0, END)
        entry_contact.delete(0, END)
        load_patients()
    else:
        messagebox.showwarning("Warning", "All fields are required!")

def delete_patient():
    selected_item = listbox.curselection()
    if selected_item:
        patient_id = listbox.get(selected_item).split(" - ")[0]  
        cursor.execute("DELETE FROM patients WHERE id=?", (patient_id,))
        conn.commit()
        load_patients()
    else:
        messagebox.showwarning("Warning", "Select a patient to delete!")

def load_patients():
    listbox.delete(0, END)
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    for patient in patients:
        listbox.insert(END, f"{patient[0]} - {patient[1]} | Age: {patient[2]} | {patient[3]} | {patient[4]}")

# GUI Setup
app = Tk()
app.title("Hospital Management System")
app.geometry("600x500")

Label(app, text="Patient Name:").pack()
entry_name = Entry(app)
entry_name.pack()

Label(app, text="Age:").pack()
entry_age = Entry(app)
entry_age.pack()

Label(app, text="Disease:").pack()
entry_disease = Entry(app)
entry_disease.pack()

Label(app, text="Contact No:").pack()
entry_contact = Entry(app)
entry_contact.pack()

Button(app, text="Add Patient", command=add_patient).pack()

listbox = Listbox(app, height=10, width=60)
listbox.pack()

Button(app, text="Delete Patient", command=delete_patient, fg="red").pack()

load_patients()
app.mainloop()

conn.close()