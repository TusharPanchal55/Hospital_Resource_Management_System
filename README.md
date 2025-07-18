🏥 Hospital Resource Management System
An AI-powered web application that predicts next-day requirements for critical hospital resources such as Oxygen Cylinders, PPE Kits, and ICU Beds using past usage data. Built with Django for the backend and integrated with machine learning models to improve hospital planning and crisis readiness.

📌 Features
🔐 Role-Based Access: Secure login for Admin, Doctor, and Staff.

📊 AI Resource Forecasting: Predicts the required quantity of essential medical resources based on the past 7 days' usage.

📈 Data Dashboard: Visualizes past usage and prediction trends.

🧠 Machine Learning Integration: Built-in ML model trained on historical data for accurate forecasting.

📁 Database Management: Manages hospital resource entries with relational mapping via Django ORM.

🔄 Dynamic Input Forms: Submit and store daily usage easily.

💻 Tech Stack
Layer	Technology
Backend Framework	Django
Language	Python
Frontend	HTML, CSS, Bootstrap
ML Model	Scikit-learn, Pandas
Database	SQLite (default)
IDE	VS Code

🧠 AI Model Overview
The AI model predicts the next-day usage of:

Oxygen Cylinders

PPE Kits

ICU Beds

Algorithm Used: Linear Regression
Input: Last 7 days’ resource usage data
Output: Predicted quantity needed for the next day

📂 Project Structure
csharp
Copy
Edit
Hospital_Resource_Management_System/
├── ai_model/
│   └── predict.py               # Model logic
├── dashboard/
│   └── templates/               # HTML Templates
├── hospital/
│   ├── models.py                # Django Models
│   ├── views.py                 # Backend Logic
│   └── forms.py                 # Input Forms
├── static/                      # CSS, JS, Images
├── manage.py
└── requirements.txt
🚀 Getting Started
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/TusharPanchal55/Hospital_Resource_Management_System.git
cd Hospital_Resource_Management_System
2. Create Virtual Environment
bash
Copy
Edit
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Apply Migrations
bash
Copy
Edit
python manage.py migrate
5. Run the Server
bash
Copy
Edit
python manage.py runserver
Access the app at http://127.0.0.1:8000

👤 User Roles
Admin: Can view dashboards, manage users, and see predictions.

Doctor: Can update daily usage data and view forecasts.

Staff: Can input resource consumption data.

📸 Screenshots
<img width="1361" height="642" alt="image" src="https://github.com/user-attachments/assets/284f0d23-30c8-40f4-8cb7-384d7b2e5b00" />


🛠 Future Improvements
Add email notifications for predicted shortages.

Integrate live sensor data from hospital devices.

Deploy on cloud (e.g., AWS or Heroku).

Improve model accuracy with advanced algorithms (e.g., LSTM).

🤝 Contributions
Pull requests and feature suggestions are welcome!
Please open an issue to discuss what you'd like to change.

📄 License
This project is open-source under the MIT License.
