# **Movie Ticket Booking System**

- ## **Project Description and Discussion file:**

https://drive.google.com/file/d/1Kb4HP9OrMIsu5mcJBRtucCj93j7uyQFe/view

- ## **About the Project:**

This project is the backend implementation of a Movie ticket booking system.This projects implements the various business cases required for successful running of a Movie ticket booking system. It has been implemented using three tables namely:
 - **User Table** (customer_id,name ,phone_number) : stores details of customers
 - **MovieShow Table** (timings, tickets available) : stores details about movies
 - **Ticket Table** (ticket_id, time_of_movie, customer_id, hasexpired) : stores details of tickets sold
 
  Please check the above link for detailed implementation of database schema.

- ## **Built with:**

This project has been implemented using **Flask** backend and database used is **Sqlite3**, the queries have been written in Flask using **SQLAlchemy** library.

- ## **Installation:**
1)	Download or clone the project using the web URL.
2)	Open app.py file in backend folder, add your database path to the variable app.config[SQLALCHEMY_DATABASE_URI ]= “sqlite:///your_file_path”.
3)	Install the requirements from requirements.txt file.
4)	To run the project, open your terminal, go to your folder containing the main.py file and backend folder  and type –“python main.py”.
5)	The project will be deployed on localhost:5000.
6)	You can use Postman or any other application for sending requests to various urls’.

- ## **Folder Structure:**
 - **Main Folder:**
   - backend folder:
      - app.py-app configurations set here
      - models.py-schema of the tables is defined in this file
      - functions.py- contains all the functions implementing the given business cases
      - ticketbooking.db- sqlite database containing the tables 
                      
   - main.py
	

- ## **Running the tests:**

Detailed description of the tests and the code is given in the file attached under the heading -**'Project Description and Discussion file'**.
