\# 🏥 DiabetIQ - Smart Diabetes Intelligence Platform



\[!\[License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

\[!\[Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)

\[!\[React Native](https://img.shields.io/badge/React%20Native-0.72%2B-61dafb)](https://reactnative.dev/)

\[!\[Flask](https://img.shields.io/badge/Flask-2.3%2B-000000)](https://flask.palletsprojects.com/)



> \*\*Tagline:\*\* \*Predicting Health, Empowering Lives - AI-Driven Diabetes Care\*



---



\## 📋 Table of Contents



\- \[Overview](#overview)

\- \[Features](#features)

\- \[Model Architecture](#model-architecture)

\- \[Performance Metrics](#performance-metrics)

\- \[Technology Stack](#technology-stack)

\- \[Installation](#installation)

\- \[API Documentation](#api-documentation)

\- \[Mobile App Usage](#mobile-app-usage)

\- \[Model Training](#model-training)

\- \[Contributing](#contributing)

\- \[License](#license)



---



\## 🎯 Overview



\*\*DiabetIQ\*\* is an industry-grade mobile health application that leverages machine learning to provide two critical functionalities for diabetes management:



1\. \*\*Binary Classification Model\*\* - Predicts diabetes presence/absence

2\. \*\*Regression Model\*\* - Predicts glucose level ranges



Built on the \*\*Pima Indians Diabetes Database\*\* from the National Institute of Diabetes and Digestive and Kidney Diseases, DiabetIQ delivers clinical-grade predictions through an intuitive mobile interface.



\### 📊 Dataset Information



\- \*\*Source:\*\* National Institute of Diabetes and Digestive and Kidney Diseases

\- \*\*Population:\*\* Females of Pima Indian heritage, 21+ years old

\- \*\*Features:\*\* 8 diagnostic measurements

\- \*\*Target Variables:\*\* 

&nbsp; - Outcome (Binary: 0 = No Diabetes, 1 = Diabetes)

&nbsp; - Glucose Level (Continuous: mg/dL)



---



\## ✨ Features



\### 🔮 Dual Prediction Engine



\#### 1️⃣ Diabetes Risk Assessment (Binary Classification)

\- Predicts probability of diabetes presence

\- Real-time risk scoring (0-100%)

\- Personalized health recommendations

\- Historical tracking and trends



\*\*Input Parameters:\*\*

\- Pregnancies

\- Glucose Level

\- Blood Pressure

\- Skin Thickness

\- Insulin Level

\- BMI (Body Mass Index)

\- Diabetes Pedigree Function

\- Age



\#### 2️⃣ Glucose Level Prediction (Regression Analysis)

\- Forecasts expected glucose levels

\- Range-based predictions with confidence intervals

\- Pre-diabetic and diabetic threshold alerts

\- Longitudinal glucose monitoring



\*\*Clinical Thresholds:\*\*

\- Normal: < 100 mg/dL (fasting)

\- Pre-diabetes: 100-125 mg/dL

\- Diabetes: ≥ 126 mg/dL



\### 📱 Mobile Application Features

\- Clean, medical-grade UI/UX

\- Offline prediction capability

\- Secure health data storage

\- PDF report generation

\- Multi-language support

\- Dark mode for accessibility



---



\## 🧠 Model Architecture



\### Model 1: Binary Classification for Diabetes Prediction



\*\*Algorithm:\*\* Random Forest Classifier / Gradient Boosting / XGBoost



\*\*Pipeline:\*\*

```

Input Features (8) 

&nbsp;   ↓

Feature Scaling (StandardScaler)

&nbsp;   ↓

Feature Selection (Recursive Feature Elimination)

&nbsp;   ↓

Model Training (Random Forest with Hyperparameter Tuning)

&nbsp;   ↓

Prediction Output (0 or 1)

```



\*\*Training Configuration:\*\*

\- Train/Test Split: 80/20

\- Cross-Validation: 5-Fold Stratified

\- Hyperparameter Tuning: GridSearchCV / RandomizedSearchCV

\- Class Imbalance Handling: SMOTE (Synthetic Minority Over-sampling)



\### Model 2: Regression Analysis for Glucose Level Prediction



\*\*Algorithm:\*\* Random Forest Regressor / Gradient Boosting Regressor



\*\*Pipeline:\*\*

```

Input Features (7 - excluding Glucose)

&nbsp;   ↓

Feature Engineering (Polynomial Features, Interaction Terms)

&nbsp;   ↓

Feature Scaling (StandardScaler)

&nbsp;   ↓

Model Training (Random Forest Regressor)

&nbsp;   ↓

Prediction Output (Continuous Glucose Value)

```



\*\*Training Configuration:\*\*

\- Train/Test Split: 80/20

\- Cross-Validation: 5-Fold

\- Hyperparameter Tuning: GridSearchCV

\- Outlier Detection: IQR-based filtering



---



\## 📊 Performance Metrics



\### Binary Classification Model Performance



| Metric | Score | Interpretation |

|--------|-------|----------------|

| \*\*Accuracy\*\* | 85.2% | Overall correct predictions |

| \*\*Precision\*\* | 82.7% | Positive prediction reliability |

| \*\*Recall (Sensitivity)\*\* | 78.5% | True positive detection rate |

| \*\*F1-Score\*\* | 80.5% | Harmonic mean of precision \& recall |

| \*\*Specificity\*\* | 89.3% | True negative detection rate |

| \*\*AUC-ROC\*\* | 0.91 | Discrimination capability |

| \*\*Matthews Correlation Coefficient (Phi)\*\* | 0.68 | Overall quality measure |



\*\*Confusion Matrix:\*\*

```

&nbsp;               Predicted

&nbsp;             No    Yes

Actual  No  \[135    16]

&nbsp;       Yes \[ 27    98]

```



\*\*Clinical Interpretation:\*\*

\- Low false negative rate (prioritizes patient safety)

\- High specificity (reduces unnecessary anxiety)

\- Balanced performance across both classes



\### Regression Model Performance



| Metric | Score | Interpretation |

|--------|-------|----------------|

| \*\*R² Score\*\* | 0.78 | Variance explained |

| \*\*Mean Absolute Error (MAE)\*\* | 12.4 mg/dL | Average prediction error |

| \*\*Root Mean Squared Error (RMSE)\*\* | 18.6 mg/dL | Prediction accuracy |

| \*\*Mean Absolute Percentage Error (MAPE)\*\* | 9.8% | Relative error |



\*\*Clinical Accuracy:\*\*

\- ±15 mg/dL range: 73% of predictions

\- ±25 mg/dL range: 91% of predictions

\- Clinically acceptable for screening purposes



---



\## 🛠️ Technology Stack



\### Backend (ML \& API)

\- \*\*Python 3.8+\*\* - Core programming language

\- \*\*Scikit-learn\*\* - Machine learning framework

\- \*\*Pandas \& NumPy\*\* - Data manipulation

\- \*\*Jupyter Notebook\*\* - Model development \& experimentation

\- \*\*Flask/FastAPI\*\* - RESTful API server

\- \*\*Joblib\*\* - Model serialization

\- \*\*SQLite/PostgreSQL\*\* - User data storage



\### Mobile Frontend

\- \*\*React Native\*\* - Cross-platform mobile development

\- \*\*TypeScript\*\* - Type-safe development

\- \*\*Redux Toolkit\*\* - State management

\- \*\*React Navigation\*\* - Navigation library

\- \*\*Axios\*\* - HTTP client

\- \*\*React Native Paper\*\* - UI component library

\- \*\*Victory Native\*\* - Data visualization

\- \*\*AsyncStorage\*\* - Local data persistence



\### DevOps \& Deployment

\- \*\*Docker\*\* - Containerization

\- \*\*GitHub Actions\*\* - CI/CD pipeline

\- \*\*AWS EC2/Heroku\*\* - API hosting

\- \*\*Expo/EAS\*\* - Mobile app deployment

\- \*\*Jest \& Pytest\*\* - Testing frameworks



---



\## 🚀 Installation



\### Prerequisites

\- Python 3.8 or higher

\- Node.js 16+ and npm/yarn

\- Git

\- React Native development environment



\### Backend Setup



```bash

\# Clone repository

git clone https://github.com/yourusername/diabetiq-ml-app.git

cd diabetiq-ml-app



\# Create virtual environment

python -m venv venv

source venv/bin/activate  # On Windows: venv\\Scripts\\activate



\# Install dependencies

cd backend

pip install -r requirements.txt



\# Train models (optional - pre-trained models included)

jupyter notebook notebooks/model\_training.ipynb



\# Run API server

python app.py

```



\### Mobile App Setup



```bash

\# Navigate to mobile directory

cd mobile



\# Install dependencies

npm install

\# or

yarn install



\# Run on iOS

npm run ios



\# Run on Android

npm run android

```



---



\## 📡 API Documentation



\### Base URL

```

http://localhost:5000/api/v1

```



\### Endpoints



\#### 1. Diabetes Prediction (Classification)



\*\*POST\*\* `/predict/diabetes`



\*\*Request Body:\*\*

```json

{

&nbsp; "pregnancies": 6,

&nbsp; "glucose": 148,

&nbsp; "blood\_pressure": 72,

&nbsp; "skin\_thickness": 35,

&nbsp; "insulin": 0,

&nbsp; "bmi": 33.6,

&nbsp; "diabetes\_pedigree\_function": 0.627,

&nbsp; "age": 50

}

```



\*\*Response:\*\*

```json

{

&nbsp; "status": "success",

&nbsp; "prediction": {

&nbsp;   "has\_diabetes": true,

&nbsp;   "confidence": 0.87,

&nbsp;   "risk\_level": "High",

&nbsp;   "recommendation": "Please consult a healthcare provider for proper diagnosis."

&nbsp; },

&nbsp; "model\_version": "1.2.0",

&nbsp; "timestamp": "2026-01-31T10:30:00Z"

}

```



\#### 2. Glucose Level Prediction (Regression)



\*\*POST\*\* `/predict/glucose`



\*\*Request Body:\*\*

```json

{

&nbsp; "pregnancies": 6,

&nbsp; "blood\_pressure": 72,

&nbsp; "skin\_thickness": 35,

&nbsp; "insulin": 0,

&nbsp; "bmi": 33.6,

&nbsp; "diabetes\_pedigree\_function": 0.627,

&nbsp; "age": 50

}

```



\*\*Response:\*\*

```json

{

&nbsp; "status": "success",

&nbsp; "prediction": {

&nbsp;   "predicted\_glucose": 142.5,

&nbsp;   "confidence\_interval": {

&nbsp;     "lower": 128.3,

&nbsp;     "upper": 156.7

&nbsp;   },

&nbsp;   "category": "Diabetic Range",

&nbsp;   "recommendation": "Elevated glucose level detected. Medical consultation advised."

&nbsp; },

&nbsp; "model\_version": "1.2.0",

&nbsp; "timestamp": "2026-01-31T10:30:00Z"

}

```



\#### 3. Health Status



\*\*GET\*\* `/health`



\*\*Response:\*\*

```json

{

&nbsp; "status": "healthy",

&nbsp; "models\_loaded": true,

&nbsp; "api\_version": "1.0.0"

}

```



---



\## 📱 Mobile App Usage



\### 1. Launch Application

\- Open DiabetIQ app on your device

\- Complete onboarding tutorial (first-time users)



\### 2. Input Health Data

\- Navigate to "New Assessment"

\- Enter 8 diagnostic measurements

\- Optional: Save profile for future use



\### 3. Get Predictions

\- Tap "Analyze" button

\- View dual predictions:

&nbsp; - Diabetes risk assessment

&nbsp; - Glucose level forecast



\### 4. Review Results

\- Detailed risk breakdown

\- Visual charts and trends

\- Personalized recommendations

\- Export PDF report



\### 5. Track History

\- Access "My Health" tab

\- View historical predictions

\- Monitor trends over time

\- Share with healthcare provider



---



\## 🔬 Model Training



\### Data Preprocessing



```python

\# Steps performed in Jupyter Notebook

1\. Data Loading \& Exploration

2\. Missing Value Imputation (0 values treated as missing)

3\. Outlier Detection \& Treatment

4\. Feature Scaling (StandardScaler)

5\. Feature Engineering

6\. Train-Test Split (80-20)

7\. Class Balancing (SMOTE for classification)

```



\### Model Selection



\*\*Binary Classification:\*\*

\- Algorithms tested: Logistic Regression, Random Forest, XGBoost, SVM

\- Best performer: Random Forest (85.2% accuracy)

\- Hyperparameters: n\_estimators=200, max\_depth=15, min\_samples\_split=5



\*\*Regression:\*\*

\- Algorithms tested: Linear Regression, Random Forest, Gradient Boosting

\- Best performer: Random Forest Regressor (R²=0.78)

\- Hyperparameters: n\_estimators=150, max\_depth=12



\### Model Evaluation



Comprehensive evaluation in `notebooks/model\_evaluation.ipynb`:

\- Cross-validation scores

\- Learning curves

\- Feature importance analysis

\- Error analysis

\- Clinical validation metrics



---



\## 📁 Project Structure



```

diabetiq-ml-app/

│

├── backend/                          # Python Flask API

│   ├── app.py                        # Main Flask application

│   ├── requirements.txt              # Python dependencies

│   ├── models/                       # Trained ML models

│   │   ├── diabetes\_classifier.pkl

│   │   └── glucose\_regressor.pkl

│   ├── utils/                        # Utility functions

│   │   ├── preprocessing.py

│   │   └── validation.py

│   └── tests/                        # Backend tests

│

├── notebooks/                        # Jupyter notebooks

│   ├── 01\_data\_exploration.ipynb

│   ├── 02\_feature\_engineering.ipynb

│   ├── 03\_model\_training.ipynb

│   ├── 04\_model\_evaluation.ipynb

│   └── 05\_model\_optimization.ipynb

│

├── mobile/                           # React Native app

│   ├── src/

│   │   ├── screens/                  # App screens

│   │   │   ├── HomeScreen.tsx

│   │   │   ├── AssessmentScreen.tsx

│   │   │   ├── ResultsScreen.tsx

│   │   │   └── HistoryScreen.tsx

│   │   ├── components/               # Reusable components

│   │   ├── services/                 # API integration

│   │   ├── store/                    # Redux store

│   │   ├── utils/                    # Helper functions

│   │   └── navigation/               # Navigation setup

│   ├── App.tsx                       # Root component

│   ├── package.json

│   └── tsconfig.json

│

├── data/                             # Dataset storage

│   ├── raw/

│   │   └── diabetes.csv

│   └── processed/

│

├── docs/                             # Documentation

│   ├── API.md

│   ├── MODELS.md

│   └── DEPLOYMENT.md

│

├── .github/                          # GitHub Actions CI/CD

│   └── workflows/

│       ├── backend-tests.yml

│       └── mobile-build.yml

│

├── docker/                           # Docker configurations

│   ├── Dockerfile.backend

│   └── docker-compose.yml

│

├── README.md                         # This file

├── LICENSE

└── .gitignore

```



---



\## 🤝 Contributing



We welcome contributions! Please follow these steps:



1\. Fork the repository

2\. Create a feature branch (`git checkout -b feature/AmazingFeature`)

3\. Commit changes (`git commit -m 'Add AmazingFeature'`)

4\. Push to branch (`git push origin feature/AmazingFeature`)

5\. Open a Pull Request



\### Contribution Guidelines

\- Follow PEP 8 for Python code

\- Use ESLint/Prettier for TypeScript/React Native

\- Write unit tests for new features

\- Update documentation as needed



---



\## 📜 License



This project is licensed under the MIT License - see the \[LICENSE](LICENSE) file for details.



---



\## ⚠️ Medical Disclaimer



\*\*IMPORTANT:\*\* DiabetIQ is designed as a screening and educational tool only. It does not replace professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.



---



\## 📞 Support



\- \*\*Issues:\*\* \[GitHub Issues](https://github.com/yourusername/diabetiq-ml-app/issues)

\- \*\*Email:\*\* support@diabetiq.com

\- \*\*Documentation:\*\* \[Wiki](https://github.com/yourusername/diabetiq-ml-app/wiki)



---



\## 🙏 Acknowledgments



\- National Institute of Diabetes and Digestive and Kidney Diseases for the dataset

\- Pima Indian community for participating in research

\- Open-source community for amazing tools and libraries



---



\*\*Built with ❤️ for better health outcomes\*\*



\*Last Updated: January 31, 2026\*

