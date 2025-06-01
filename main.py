import mysql.connector, csv, time
from tkinter import ttk, messagebox, filedialog, PhotoImage
from tkinter import *
from ttkthemes import ThemedTk
from PIL import Image, ImageTk

# ---------- Database Classes ----------

class StudentDatabase:
    def __init__(self, host='localhost', user='root', password='root', database='student_db'):
        self.conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100), course VARCHAR(45), semester VARCHAR(45),
                year INT, email VARCHAR(45), score INT, grade VARCHAR(5)
            )
        """)
        self.conn.commit()

    def add(self, name, course, semester, year, email, score, grade):
        self.cursor.execute("INSERT INTO students (name, course, semester, year, email, score, grade) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                            (name, course, semester, int(year), email, int(score), grade))
        self.conn.commit()

    def update(self, student_id, name, course, semester, year, email, score, grade):
        self.cursor.execute("UPDATE students SET name=%s, course=%s, semester=%s, year=%s, email=%s, score=%s, grade=%s WHERE id=%s",
                            (name, course, semester, int(year), email, int(score), grade, int(student_id)))
        self.conn.commit()

    def delete(self, student_id):
        self.cursor.execute("DELETE FROM students WHERE id=%s", (student_id,))
        self.conn.commit()

    def search_by_course(self, keyword):
        self.cursor.execute("SELECT * FROM students WHERE course LIKE %s", (f"%{keyword}%",))
        return self.cursor.fetchall()

    def search(self, keyword):
        self.cursor.execute("SELECT * FROM students WHERE name LIKE %s", (f"%{keyword}%",))
        return self.cursor.fetchall()

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM students")
        return self.cursor.fetchall()

    def grade(self, score):
        try:
            score = int(score)
        except ValueError:
            return "F"
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        return 'F'

    def export(self, filepath):
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Name', 'Course', 'Semester', 'Year', 'Email', 'Score', 'Grade'])
            writer.writerows(self.fetch_all())

    def close(self):
        self.cursor.close()
        self.conn.close()

class AdminDatabase:
    def __init__(self, host='localhost', user='root', password='root', database='student_db'):
        self.conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        self.cursor = self.conn.cursor()

    def validate_user(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        return self.cursor.fetchone() is not None

    def close(self):
        self.cursor.close()
        self.conn.close()

# ---------- GUI Classes ----------

class AdminLogin:
    def __init__(self, master):
        self.master = master
        master.title("Login - ReDI School Student Management System")
        master.geometry('1350x900+0+0')  #This is the dimension of the AdminLogin page
        master.resizable(False, False)   #This code disabled resizing of the page

        image = Image.open("project/rediBanner.jpg")  
        backgroundImage = ImageTk.PhotoImage(image)  #imageTk was used because picture is in '.jpg'

        backgroundLabel = Label(master, image=backgroundImage)
        backgroundLabel.place(x=0, y=0)
        backgroundLabel.image = backgroundImage

        self.user_db = AdminDatabase()

        self.frame = Frame(master, padx=20, pady=20)
        self.frame.pack(expand=True)

        Label(self.frame, text="Username:", font=("Arial", 12)).grid(row=0, column=0, sticky=W, pady=10)
        self.username_entry = Entry(self.frame, font=("Arial", 12))
        self.username_entry.grid(row=0, column=1, pady=10)

        Label(self.frame, text="Password:", font=("Arial", 12)).grid(row=1, column=0, sticky=W, pady=10)
        self.password_entry = Entry(self.frame, show="*", font=("Arial", 12))
        self.password_entry.grid(row=1, column=1, pady=10)

        self.show_var = IntVar()
        Checkbutton(self.frame, text="Show Password", variable=self.show_var, command=self.toggle_password).grid(row=2, columnspan=2)

        Button(self.frame, text="Login", command=self.check_login, font=("Arial", 12)).grid(row=3, columnspan=2, pady=20)

        Button(self.frame, text="Forgot Password?", font=("Arial", 10), fg="#58ADC5", relief=FLAT,
               command=self.forgot_password).grid(row=4, columnspan=2)

    def toggle_password(self):
        self.password_entry.config(show="" if self.show_var.get() else "*")

    def check_login(self):
        if self.user_db.validate_user(self.username_entry.get(), self.password_entry.get()):
            self.user_db.close()
            self.master.destroy()
            main()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def forgot_password(self):
        messagebox.showinfo("Not Implemented", "Password recovery is not implemented yet.")

class ReDISchoolApp:
    def __init__(self, master):
        self.db = StudentDatabase()
        self.master = master
        master.title('ReDI School student Management System')
        master.geometry('1350x800+0+0')

        top_frame = Frame(master,bg="#58ADC5",height=50)
        top_frame.pack(fill=X) 

        #Slider to make name marquee, to improve visual effect
        self.slider_text = "ReDI School Student Management System           "
        self.slider_label = Label(top_frame, text=self.slider_text, font=("Arial", 20, "bold"), fg="#58ADC5")
        self.slider_label.pack(side=LEFT)

        self.time_label = Label(top_frame, font=("Arial", 12), fg="#EA5B25")
        self.time_label.pack(side=RIGHT, padx=10)

        self.update_time()
        
        self.slider()

        # --- Main Layout ---
        main_frame = Frame(master)
        main_frame.pack(fill=BOTH, expand=True)

        left_frame = Frame(main_frame, width=200, bg="#DADADA")
        left_frame.pack(side=LEFT, fill=Y)
        right_frame = Frame(main_frame)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        try:
            self.logo_image = PhotoImage(file="project/redilogo.png")
            Label(left_frame, image=self.logo_image, bg='#DADADA').pack(pady=20)
        except:
            Label(left_frame, text="Logo", bg="#DADADA").pack(pady=20)

        for text, command in [
            ('Add Student', self.add_student),
            ('Update Student', self.update_student),
            ('Search Student', self.search_student),
            ('Delete Student', self.delete_student),
            ('View StudentData', self.show_students),
            ('Export', self.export_studentData),
            ('Exit', self.exit_app),
        ]:
            Button(left_frame, text=text, command=command, width=20).pack(pady=10)

        # --- Student Data Entry Section---
        input_frame = Frame(right_frame)
        input_frame.pack(pady=10)

        self.entries = {}
        for i, field in enumerate(['ID', 'Name', 'Course','Semester(Spring/Winter)','Year', 'Email', 'Score']):
            Label(input_frame, text=field).grid(row=i, column=0, sticky=W, padx=5, pady=3)
            self.entries[field] = Entry(input_frame)
            self.entries[field].grid(row=i, column=1, padx=5)

        # --- Table Section for Student Data Display ---
        table_frame = Frame(right_frame)
        table_frame.pack(fill=BOTH, expand=True)
         
        #scroll to navigate x and y axis in the tree view
        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        self.tree = ttk.Treeview(
            table_frame, columns=('ID','Name','Course','Semester','Year','Email','Score','Grade'),
            show='headings', xscrollcommand=scroll_x.set, 
                             yscrollcommand=scroll_y.set)

        scroll_x.config(command=self.tree.xview)
        scroll_y.config(command=self.tree.yview)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        self.tree.pack(fill=BOTH, expand=True)
        
        #overwrite theme to change background colour of table column header
        style = ttk.Style()
        style.configure("Treeview", 
                        background="#58ADC5", 
                        foreground="#CDE6EE", 
                        rowheight=25, 
                        fieldbackground="CDE6EE")
        style.map('Treeview', background=[('selected','#58ADC5')])

        for col in self.tree['columns']:
            self.tree.heading(col, text=col, anchor=CENTER)
            self.tree.column(col, anchor=CENTER, width=100)

        self.show_students()
    
    # ----slider function -----
    def slider(self):
        text = self.slider_text
        self.slider_text = text[1:] + text[0] 
        self.slider_label.config(text=self.slider_text)
        self.master.after(200, self.slider) 
    
    #---function to update time displayed every second
    def update_time(self):
        self.time_label.config(text=time.strftime('%d-%m-%Y     %H:%M:%S'))
        self.master.after(1000, self.update_time)

    #this funtion allows data entry from app user
    def get_inputs(self):
        return [e.get().strip() for e in self.entries.values()]

    #clear inout field
    def clear_fields(self):
        for e in self.entries.values():
            e.delete(0, END)

   #Validates and inserts a new student into the database.
    def add_student(self):
        data = self.get_inputs()[1:]
        if not all(data):
            messagebox.showwarning("Input Error", "Please fill missing fields")
            return
        try:
            grade = self.db.grade(data[-1])
            self.db.add(*data, grade)
            self.show_students()
            self.clear_fields()
            messagebox.showinfo("Success", "New Student added.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # --- This function update student data in the database when a change is made in the form
    def update_student(self):
        sid, *data = self.get_inputs()
        if not all([sid] + data):
            messagebox.showwarning("Input Error", "Please fill missing fields")
            return
        try:
            grade = self.db.grade(data[-1])
            self.db.update(sid, *data, grade)
            self.show_students()
            self.clear_fields()
            student_id = f"{sid[0]}"
            messagebox.showinfo("Success", f"Student with id: {student_id} has been updated.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---- This function removes student from the database with their ID
    def delete_student(self):
        sid = self.entries['ID'].get()
        if sid:
            self.db.delete(sid)
            self.show_students()
            self.clear_fields()
            student_id = f"{sid[0]}"
            messagebox.showinfo("Success", f"Student with id: {student_id} deleted:")
        else:
            messagebox.showwarning("Input Error", "Please enter student ID")

    # ---- this function allows student to be searched by their Names
    def search_student(self):
        keyword = self.entries['Name'].get()
        results = self.db.search(keyword)
        self.tree.delete(*self.tree.get_children())
        for row in results:
            self.tree.insert('', 'end', values=row)

    # ---- This function displays all students in the database
    def show_students(self):
        self.tree.delete(*self.tree.get_children())
        for row in self.db.fetch_all():
            self.tree.insert('', 'end', values=row)

    # ---- This function allows us to Transfer studentData in a CSV file to an external location
    def export_studentData(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if path:
            self.db.export(path)
            messagebox.showinfo("Exported", f"Data saved to {path}")

    def exit_app(self):
        self.db.close()
        self.master.destroy()

# ---------- Main funtion ----------

def main():
    root = ThemedTk(theme="arc")
    ReDISchoolApp(root)
    root.mainloop()

if __name__ == '__main__':
    login_root = Tk()
    AdminLogin(login_root)
    login_root.mainloop()
