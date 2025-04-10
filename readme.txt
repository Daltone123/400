============================================================
Dira Farm - AI-Powered Potato Disease Diagnosis System
============================================================

STUDENT DETAILS:
----------------
Name:         Daltone Otieno  
Reg. Number:  J31/3609/2021  
Supervisor:   Dr. Abraham Mutua  

PROJECT OVERVIEW:
-----------------
Dira Farm is an AI-powered web-based system that helps small-scale potato farmers diagnose common potato diseases such as Early Blight and Late Blight. The system uses image-based machine learning to classify diseases and provide treatment guidance. Additionally, it assists users in locating nearby agrovets and accessing educational material.

It integrates:
- FastAPI for machine learning model serving.
- Django for backend web logic and database interactions.
- JavaScript, HTML, and CSS for the interactive frontend.
- MySQL for persistent data storage.

INSTALLATION INSTRUCTIONS:
--------------------------
To set up and run the project locally, follow these steps:

1. Clone or Copy the Project:
   - From GitHub:
     ```bash
     git clone https://github.com/Daltone123/400
     cd 400
     ```
   - Or copy the folder directly from this CD.

2. Set Up the Python Virtual Environment:
   - Ensure Python 3.10 or newer is installed.
   - Create the virtual environment:
     ```bash
     python -m venv venv
     ```
   - Activate it:
     - On Windows:
       ```bash
       venv\Scripts\activate
       ```
     - On Linux/Mac:
       ```bash
       source venv/bin/activate
       ```

3. Install Required Dependencies:
   ```bash
   pip install -r requirements.txt


4. Set Up the MySQL Database:
Make sure MySQL is installed and running.
Create a database (e.g., dirafarm) and import the SQL file provided in the database/ folder:
CREATE DATABASE dirafarm;
USE dirafarm;
SOURCE /path/to/database/dirafarm.sql;

5. Run Django migrations and server:

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

6. Frontend Setup:

- No additional build tools are required.

- Frontend files (HTML, CSS, JavaScript) are located within the Django project directories or templates/static folders.

- The frontend interacts with Django and FastAPI via HTTP requests.

7. Run the System:

From the project root directory (where manage.py is located), run:

python manage.py runserver

8. Open the browser and go to:

http://127.0.0.1:8000/





