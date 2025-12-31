# Big Mart Sales Prediction

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Scikit%20Learn-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## 📌 Project Overview

**Big Mart Sales Prediction** is a machine learning-powered web application designed to forecast sales for various items across different Big Mart outlets. By leveraging historical sales data, the application predicts future sales figures based on item attributes (like weight, fat content, visibility) and outlet characteristics (like size, location, and type).

This project aims to assist store managers and business analysts in optimizing inventory management and sales strategies.

## ✨ Features

-   **User Authentication**: Secure Login and Registration system for authorized access.
-   **Intelligent Predictions**: Input product and store details to get instant sales forecasts using a trained XGBoost/Linear Regression model.
-   **Interactive Dashboard**: Visualize sales trends, item performance, and outlet statistics with dynamic charts.
-   **Feedback System**: Users can submit feedback directly through the application.
-   **RESTful API**: Exposes an endpoint (`/api/predict`) for external integrations.
-   **Welcome Emails**: Automated email notifications upon successful user registration.

## 🛠️ Technology Stack

-   **Backend**: Flask (Python)
-   **Database**: SQLite (SQLAlchemy ORM)
-   **Machine Learning**: Scikit-Learn, Pandas, NumPy, Pickle
-   **Frontend**: HTML5, CSS3, Jinja2 Templates
-   **Data Visualization**: Chart.js (or similar) on the dashboard

## 🚀 Installation & Setup

Follow these steps to get the project running on your local machine.

### Prerequisites
-   Python 3.8 or higher
-   Git

### 1. Clone the Repository
```bash
git clone https://github.com/raj6297bahu/Bigmart.AI.git
cd Big-mart-sales-prediction
```

### 2. Create a Virtual Environment
It's recommended to use a virtual environment to manage dependencies.
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add the following configurations:
```env
SECRET_KEY=your_secret_key_here
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_email_app_password
```
> **Note**: For email functionality to work, you may need an App Password if using Gmail.

### 5. Run the Application
```bash
python app.py
```
 The application will allow be accessible at `http://localhost:8000`.

## 📖 Usage

1.  **Register/Login**: Create an account or log in to access the main features.
2.  **Make a Prediction**:
    -   Navigate to the "Predict" page.
    -   Fill in the details regarding the Item (Fat Content, Type, MRP) and Outlet (Size, Location, Type).
    -   Click "Predict" to see the estimated sales.
3.  **View Dashboard**: Check the "Dashboard" tab for visual insights into the data.
4.  **API Usage**:
    -   Send a POST request to `/api/predict` with JSON data:
    ```json
    {
      "Item_Fat_Content": 0,
      "Item_Type": 4,
      "Outlet_Location_Type": 0,
      "Outlet_Type": 1,
      "Age_Outlet": 10,
      "Item_MRP": 250.0
    }
    ```

## 📂 Project Structure

```
Big-mart-sales-prediction/
├── app.py                  # Main Flask application entry point
├── requirements.txt        # Python dependencies
├── model.pkl               # Trained Machine Learning model
├── predictions.db          # SQLite database
├── templates/              # HTML Templates (Login, Predict, Dashboard, etc.)
├── static/                 # Static assets (CSS, JS, Images)
├── .env                    # Environment variables (not committed)
└── README.md               # Project documentation
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the repository.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
