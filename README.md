# 🛡️ Network Security - Phishing Detection ML Project

An end-to-end machine learning project for detecting phishing websites using various URL and domain features. The project includes data ingestion from MongoDB, data validation, transformation, model training with hyperparameter tuning, and deployment on Google Cloud Platform.

## 📋 Table of Contents

- [Overview](#overview)
- [Dataset](#dataset)
- [Project Architecture](#project-architecture)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Model Training Pipeline](#model-training-pipeline)
- [Deployment](#deployment)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)

## 🎯 Overview

This project implements a complete MLOps pipeline for phishing website detection. It uses machine learning algorithms to classify websites as legitimate or phishing based on 30 URL and domain characteristics. The system includes automated data validation, drift detection, model training with multiple algorithms, and real-time prediction capabilities through a FastAPI web application.

**Key Highlights:**

- ✅ Automated ML pipeline with data validation and drift detection
- ✅ Multiple ML algorithms with hyperparameter tuning
- ✅ MLflow integration for experiment tracking (DagsHub)
- ✅ FastAPI web interface for batch predictions
- ✅ MongoDB integration for data storage
- ✅ Google Cloud Platform deployment (Cloud Run)
- ✅ Automated CI/CD with Cloud Build

## 📊 Dataset

**Dataset:** Phishing Website Detection Dataset  
**Total Records:** 11,055 instances  
**Features:** 30 input features + 1 target variable  
**Target Variable:** `Result` (-1 for phishing, 1 for legitimate)

### Feature Categories

The dataset contains 30 features categorized into:

1. **URL Features**

   - `having_IP_Address`: Whether IP address is used instead of domain name
   - `URL_Length`: Length of the URL
   - `Shortining_Service`: Use of URL shortening services
   - `having_At_Symbol`: Presence of @ symbol in URL
   - `double_slash_redirecting`: Presence of // in URL path
   - `Prefix_Suffix`: Use of dash in domain name
   - `having_Sub_Domain`: Number of subdomains

2. **Domain Features**

   - `Domain_registeration_length`: Age of domain registration
   - `age_of_domain`: How old the domain is
   - `DNSRecord`: DNS record existence

3. **Security Features**

   - `SSLfinal_State`: SSL certificate status
   - `HTTPS_token`: HTTPS in domain part
   - `Favicon`: Favicon loaded from external domain

4. **Content Features**

   - `Request_URL`: External objects in webpage
   - `URL_of_Anchor`: Anchor tags pointing to different domain
   - `Links_in_tags`: Meta, script, and link tags from different domain
   - `SFH`: Server Form Handler
   - `Submitting_to_email`: Email submission in forms
   - `Iframe`: Use of iframe tags
   - `on_mouseover`: OnMouseOver event to hide address bar
   - `RightClick`: Right-click disabled
   - `popUpWidnow`: Pop-up windows

5. **Traffic & Ranking Features**
   - `web_traffic`: Website traffic rank
   - `Page_Rank`: Google PageRank
   - `Google_Index`: Indexed by Google
   - `Links_pointing_to_page`: Number of inbound links
   - `Statistical_report`: Listed in PhishTank, StopBadware

**Feature Values:** Most features are encoded as -1 (phishing indicator), 0 (suspicious), or 1 (legitimate indicator)

## 🏗️ Project Architecture

```
┌─────────────────┐
│   Data Source   │
│   (MongoDB)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Data Ingestion  │
│  - Fetch data   │
│  - Train/Test   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Data Validation │
│  - Schema check │
│  - Drift detect │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Transformation  │
│  - Imputation   │
│  - Scaling      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Model Training  │
│  - GridSearchCV │
│  - 6 Algorithms │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  MLflow Track   │
│  (DagsHub)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  GCP Storage    │
│  Artifacts      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Deployment    │
│  (Cloud Run)    │
└─────────────────┘
```

## ✨ Features

### 🔄 ML Pipeline Components

1. **Data Ingestion**

   - Fetches data from MongoDB
   - Exports to feature store (CSV)
   - Automatic train-test split (80:20)

2. **Data Validation**

   - Schema validation (column count, types)
   - Numerical column verification
   - Data drift detection using Kolmogorov-Smirnov test
   - Drift report generation

3. **Data Transformation**

   - KNN Imputer for missing values (k=3)
   - RobustScaler for feature scaling
   - Preprocessing pipeline saved as artifact

4. **Model Training**

   - Multiple algorithms with hyperparameter tuning:
     - Logistic Regression
     - K-Nearest Neighbors
     - Decision Tree
     - AdaBoost
     - Gradient Boosting
     - Random Forest
   - Grid Search Cross-Validation
   - Best model selection based on F1-score
   - Detailed classification metrics (F1, Precision, Recall)

5. **MLflow Tracking**

   - Experiment tracking with DagsHub
   - Metric logging (F1, Precision, Recall for train/test)
   - Model versioning and artifact storage

6. **Model Deployment**
   - Artifacts uploaded to GCP Storage
   - Model and preprocessor saved for inference

## 🚀 Installation

### Prerequisites

- Python 3.10+
- MongoDB database
- Google Cloud Platform account (for deployment)
- DagsHub account (for MLflow tracking)

### Local Setup

1. **Clone the repository**

```bash
git clone <repository-url>
cd NetworkSecurity
```

2. **Create virtual environment**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory:

```env
# MongoDB Configuration
MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority

# DagsHub/MLflow Configuration
DAGSHUB_TOKEN=your_dagshub_token_here

# Google Cloud (for deployment)
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account-key.json
```

5. **Load data to MongoDB**

```bash
python mongo/load_data.py
```

## 💻 Usage

### Running Locally

```bash
python app.py
```

The application will start at `http://localhost:8080`

### Using Docker

```bash
# Build image
docker build -t network-security:latest .

# Run container
docker run -p 8080:8080 \
  -e DAGSHUB_TOKEN=your_token \
  network-security:latest
```

## 🔌 API Endpoints

### 1. Home Page

```http
GET /
```

Returns the web interface for file upload and batch prediction.

### 2. Train Model

```http
GET /train
```

Triggers the complete ML training pipeline:

- Data ingestion from MongoDB
- Data validation and drift detection
- Data transformation
- Model training with hyperparameter tuning
- Artifact upload to GCP

**Response:**

```json
{
  "message": "Training successful",
  "model_trainer_artifact": {...}
}
```

### 3. Load Data to MongoDB

```http
GET /load_data
```

Loads data from CSV to MongoDB database.

**Response:**

```json
{
  "message": "ETL pipeline successful"
}
```

### 4. Batch Prediction

```http
POST /predict
Content-Type: multipart/form-data
```

Upload a CSV file for batch predictions.

**Request:**

- Form data with CSV file

**Response:**
HTML table with predictions added as a new column.

## 🔄 Model Training Pipeline

### Pipeline Flow

```python
from networksecurity.pipeline.training_pipeline import TrainingPipeline

# Initialize pipeline
pipeline = TrainingPipeline()

# Run complete pipeline
artifact = pipeline.run_pipeline()
```

### Pipeline Stages

1. **Data Ingestion** → Fetches data from MongoDB, splits into train/test
2. **Data Validation** → Validates schema, checks drift (threshold: 0.05)
3. **Data Transformation** → Imputes missing values, scales features
4. **Model Training** → Trains 6 models, selects best based on F1-score
5. **Artifact Upload** → Uploads models and artifacts to GCP Storage

### Model Selection Process

The pipeline trains 6 different algorithms with hyperparameter tuning:

- **Logistic Regression**: Linear classification baseline
- **K-Nearest Neighbors**: Instance-based learning (k=3,5,7,9,11,15)
- **Decision Tree**: Tree-based classification with depth tuning
- **AdaBoost**: Boosting ensemble (50-200 estimators)
- **Gradient Boosting**: Gradient-based ensemble (100-300 estimators)
- **Random Forest**: Bagging ensemble with multiple criteria

**Selection Criteria:** Model with highest F1-score on cross-validation

## ☁️ Deployment

### Google Cloud Platform (Cloud Run)

The project includes automated deployment configuration using Google Cloud Build.

#### Deployment Architecture

```
GitHub → Cloud Build → Artifact Registry → Cloud Run
```

#### Cloud Build Configuration

See [`cloudbuild.yaml`](cloudbuild.yaml) for complete configuration:

- **Step 1:** Build Docker image
- **Step 2:** Push to Artifact Registry
- **Step 3:** Deploy to Cloud Run with:
  - Region: us-central1
  - Port: 8080
  - Auto-scaling: 0-3 instances
  - Secrets: Service account key, DagsHub token

#### Manual Deployment

```bash
# Build and push image
gcloud builds submit --config cloudbuild.yaml

# Deploy to Cloud Run
gcloud run deploy networksecurity-ml \
  --image us-central1-docker.pkg.dev/PROJECT_ID/networksecurity-ml/networksecurity-ml-image:TAG \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## 🛠️ Technologies Used

### Core ML/AI

- **scikit-learn**: Machine learning algorithms and preprocessing
- **NumPy**: Numerical computing
- **Pandas**: Data manipulation and analysis
- **SciPy**: Statistical analysis (KS-test for drift detection)

### MLOps & Tracking

- **MLflow**: Experiment tracking and model registry
- **DagsHub**: Remote MLflow tracking server

### Web Framework

- **FastAPI**: Modern web framework for building APIs
- **Uvicorn**: ASGI server
- **Jinja2**: Template engine

### Database & Storage

- **MongoDB**: NoSQL database for data storage
- **Google Cloud Storage**: Artifact storage

### DevOps & Deployment

- **Docker**: Containerization
- **Google Cloud Run**: Serverless deployment
- **Google Cloud Build**: CI/CD pipeline

### Other Tools

- **python-dotenv**: Environment variable management
- **PyYAML**: YAML configuration parsing

## 📁 Project Structure

```
NetworkSecurity/
│
├── networksecurity/              # Main package
│   ├── components/              # Pipeline components
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   └── model_trainer.py
│   │
│   ├── pipeline/                # Pipeline orchestration
│   │   ├── training_pipeline.py
│   │   └── batch_prediction.py
│   │
│   ├── entity/                  # Data classes
│   │   ├── config_entity.py
│   │   └── artifact_entity.py
│   │
│   ├── utils/                   # Utility functions
│   │   ├── utils.py
│   │   ├── gcp_storage.py
│   │   └── ml_utils/
│   │       ├── model.py
│   │       └── metric.py
│   │
│   ├── constants/               # Constants
│   │   └── __init__.py
│   │
│   ├── exception/               # Custom exceptions
│   │   └── exception.py
│   │
│   └── logging/                 # Logging configuration
│       └── logger.py
│
├── mongo/                       # MongoDB utilities
│   ├── load_data.py
│   └── test_connect.py
│
├── Network_Data/                # Raw data
│   └── phisingData.csv
│
├── data_schemas/                # Data schemas
│   └── schema.yaml
│
├── templates/                   # HTML templates
│   ├── home.html
│   └── table.html
│
├── static/                      # Static files (CSS)
│   └── main.css
│
├── Artifacts/                   # Training artifacts (generated)
├── final_models/                # Final model files (generated)
├── mlruns/                      # MLflow local tracking (generated)
│
├── app.py                       # FastAPI application
├── requirements.txt             # Python dependencies
├── setup.py                     # Package setup
├── Dockerfile                   # Docker configuration
├── cloudbuild.yaml             # GCP Cloud Build config
└── README.md                    # This file
```

## 📊 Model Performance

The model training pipeline evaluates multiple algorithms and selects the best performer based on:

- **F1-Score**: Harmonic mean of precision and recall
- **Precision**: Accuracy of positive predictions
- **Recall**: Coverage of actual positive cases

Metrics are logged for both training and test sets in MLflow.

## 🔐 Environment Variables

| Variable                         | Description                      | Required             |
| -------------------------------- | -------------------------------- | -------------------- |
| `MONGO_URI`                      | MongoDB connection string        | Yes                  |
| `DAGSHUB_TOKEN`                  | DagsHub personal access token    | Yes (for training)   |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to GCP service account JSON | Yes (for deployment) |
| `PORT`                           | Application port                 | No (default: 8080)   |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is developed for educational purposes.

## 👤 Author

**Shri Charan**

- Email: rshricharan29@gmail.com

## 🙏 Acknowledgments

- Phishing dataset contributors
- scikit-learn community
- FastAPI framework
- DagsHub for MLflow hosting
- Google Cloud Platform

## 📞 Support

For issues and questions, please create an issue in the repository.

---

**Note:** Ensure all environment variables are properly configured before running the application. The system requires valid MongoDB connection, DagsHub token, and GCP credentials for full functionality.
