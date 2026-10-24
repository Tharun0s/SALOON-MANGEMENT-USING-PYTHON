SALON MANAGEMENT SYSTEM (HTML + INTERNAL CSS/JS + PYTHON + MYSQL)

PROJECT FILES
- app.py              Flask backend and API
- templates/index.html Frontend (HTML, CSS and JavaScript are in one file)
- schema.sql          MySQL database/table
- requirements.txt    Python packages

SETUP
1. Install Python 3.
2. Install MySQL Server and start the MySQL service.
3. Open MySQL Workbench or the MySQL command line.
4. Run the full schema.sql script to create salon_db and appointments.
5. Open app.py and update DB_CONFIG password if your MySQL root user has a password.
6. Open terminal in this project folder and run:
       python -m venv .venv
       .venv\Scripts\activate
       pip install -r requirements.txt
       python app.py
7. Open this address in your browser:
       http://127.0.0.1:5000

FEATURES
- View salon services and prices
- Book an appointment
- Save appointments to MySQL
- View saved appointments
- Delete an appointment

TROUBLESHOOTING
- If you see a database error, make sure MySQL is running, schema.sql was executed,
  and the username/password in app.py are correct.
- Keep the terminal running while using the website.
- This is a simple learning project, not a production booking system.
