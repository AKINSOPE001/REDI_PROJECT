# 🎓 ReDI School Student Management System

A comprehensive desktop application developed in Python using `Tkinter`, `MySQL`, and `ttkthemes`, designed to simplify and streamline student record management at ReDI School.

---

## 📝 Project Description

The **ReDI School Student Management System** enables efficient handling of student information such as names, courses, scores, grades, and emails. Built with a user-friendly GUI, it supports CRUD operations (Create, Read, Update, Delete), data export, and secure admin login.

---

## 🚀 Key Features

- Admin login system (with credential validation)
- Add, update, search, and delete student records
- Search students by name or course
- Auto-grade calculation based on score
- View all student records in a table (Treeview)
- Export student data to CSV format
- Marquee heading and live clock
- Input validation and error handling with try/except
- GUI with visual enhancements using ttkthemes and PIL

---

## ⚙️ Setup Instructions

1. Ensure **MySQL** is installed and running on your system.
2. Create a database in MySQL named `student_db`.
3. Create a `users` table inside `student_db` with at least one user for login:
   ```sql
   CREATE TABLE users (
     id INT AUTO_INCREMENT PRIMARY KEY,
     username VARCHAR(50),
     password VARCHAR(50)
   );
   INSERT INTO users (username, password) VALUES ('Admin', 'RediSchool');
4. Clone this repository or download the project files.

5. Install the required Python packages:
    pip install mysql-connector-python pillow ttkthemes

6.  Run the application:
    python main.py
   
7.🔐 Admin Login Credentials
Use the following credentials to access the admin panel:

Username: Admin

Password: RediSchool

⚠️ Note: The username and password are case-sensitive. Make sure to enter them exactly as shown.

## 📸 Screenshots

### 🔐 Login Screen
![Login Screenshot](https://github.com/AKINSOPE001/REDI_PROJECT/blob/main/login_screenshot.JPG)


### 🧾 Student Dashboard
![Dashboard Screenshot](https://github.com/AKINSOPE001/REDI_PROJECT/blob/main/ReDISchoolAPP_screenshot.JPG)


🤝 Acknowledgements
ReDI School Teachers and mentors

This project was inspired by the following YouTube tutorial:

- [Student Management System Tutorial](https://youtu.be/k9ICA7LDIZQ?si=lM6tCC1Le-C9Ruy7) by **Coding Lifestyle 4u**

> Special thanks for the step-by-step walkthrough that helped shape this project.

Open-source libraries (ttkthemes, Pillow)

ChatGPT for assistance in design, debugging, and documentation



🧪 Technologies Used
  Python
  
  Tkinter (GUI)
  
  MySQL (Database)
  
  ttk and Treeview (Data display)
  
  ttkthemes (Styling)
  
  PIL (Image handling)

  CSV (file export)



Developed by Akinsope Idowu, ReDI School Python(Hyrbid) student

