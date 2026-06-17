# MLOps Overview
What is MLOps?

MLOps (Machine Learning Operations) is a set of practices that combines Machine Learning, DevOps, and Data Engineering to automate and streamline the entire machine learning lifecycle.

The goal of MLOps is to make machine learning models reliable, reproducible, scalable, and easier to deploy and maintain in production environments.

MLOps Lifecycle
Data Collection
Data Validation
Data Versioning
Feature Engineering
Model Training
Model Evaluation
Model Versioning
Model Deployment
Monitoring and Observability
Continuous Retraining and Improvement
Key Benefits
Faster model development and deployment
Reproducible experiments and training runs
Automated CI/CD pipelines for ML workloads
Improved collaboration between Data Scientists, ML Engineers, and DevOps Engineers
Better model governance and traceability
Scalable and reliable production deployments

################################################################################################################################
## Data Version Control (DVC)

### Why DVC?

While all source code, configuration files, and training scripts are version-controlled using Git, machine learning datasets are often too large to store efficiently in a Git repository. Storing large datasets in Git can lead to increased repository size, slower cloning, and higher storage costs.

DVC (Data Version Control) addresses this challenge by tracking dataset versions while storing the actual data in external storage systems.

### Data Storage

Training datasets and model artifacts are stored in remote object storage such as:

* Amazon S3
* Azure Blob Storage
* Google Cloud Storage (GCS)

Git stores only lightweight metadata files, while DVC manages dataset versions and references to the actual data stored remotely.

### Benefits of DVC

* Version control for datasets and machine learning models
* Reproducible training pipelines
* Efficient storage management
* Faster Git operations
* Easy collaboration across teams
* Ability to roll back to previous dataset versions
* Seamless integration with CI/CD pipelines

### Typical Workflow

1. Add or update training data.
2. Track the dataset using DVC.
3. Push dataset changes to remote storage (S3, Azure Blob, or GCS).
4. Commit DVC metadata files to Git.
5. Team members can pull the exact dataset version using DVC for reproducible model training.

This approach keeps the Git repository lightweight while ensuring data and model versions remain fully traceable and reproducible.

################################################################################################################################

# How DVC Works

## 1. Initialize DVC

git init
dvc init

## 2. Add Dataset to DVC

dvc add data/train.csv

This creates a .dvc metadata file that is tracked in Git while the actual data remains outside Git.

## 3. Configure Remote Storage

Example: AWS S3

dvc remote add -d myremote s3://ml-project-data

Example: Azure Blob Storage

dvc remote add -d myremote azure://ml-project-data

Example: Google Cloud Storage

dvc remote add -d myremote gs://ml-project-data

## 4. Push Data to Remote Storage

dvc push

DVC uploads the dataset to the configured cloud storage.

## 5. Commit Metadata to Git

git add data/train.csv.dvc
git commit -m "Add training dataset"
git push

Only metadata is stored in Git, not the actual dataset.

## 6. Clone Project on Another Machine

git clone <repo-url>
cd project
dvc pull

DVC downloads the exact dataset version from remote storage.

## Versioning Data

When data changes:

dvc add data/train.csv
git add data/train.csv.dvc
git commit -m "Update training data"
dvc push

Now both code and data have version history.

## Tracking Models

dvc add models/model.joblib
git add models/model.joblib.dvc
git commit -m "Add trained model"
dvc push

## DVC in an MLOps Workflow

Developer
    |
    +--> Update Code --> Git
    |
    +--> Update Data --> DVC
                             |
                             +--> S3 / Azure Blob / GCS
    |
    +--> Train Model
    |
    +--> Store Model via DVC
    |
    +--> CI/CD Deploys Model

In a production MLOps setup:
- Git stores code
- DVC stores data and model metadata
- S3, Azure Blob, or GCS stores the actual datasets and model artifacts

################################################################################################################################

# Experiment Tracking

Experiment Tracking is the process of recording and managing machine learning experiments to ensure reproducibility, collaboration, and model comparison.

Data scientists often run multiple experiments while tuning hyperparameters, testing different datasets, or trying various model architectures. Experiment tracking helps maintain a complete history of these experiments.

## What Should Be Tracked?

### Parameters (Hyperparameters)

Track all model training parameters, such as:

* Learning rate
* Batch size
* Number of epochs
* Optimizer type
* Regularization parameters
* Feature selection settings

### Code Version

Track the exact code version used for training:

* Git commit hash
* Branch name
* Repository version

This ensures experiments can be reproduced using the same source code.

### Dataset Version

Track the dataset used for each experiment:

* Dataset version
* Data source
* Data preprocessing steps
* DVC version reference

This guarantees that the model can be retrained on the exact same data.

### Metrics

Record model performance metrics, such as:

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC
* Mean Squared Error (MSE)
* Root Mean Squared Error (RMSE)

Metrics help compare different experiments and select the best-performing model.

### Artifacts

Store all generated artifacts:

* Trained model files (.pkl, .joblib, .onnx)
* Feature engineering outputs
* Confusion matrices
* Training logs
* Validation reports
* Visualization plots

### System Information

Capture environment details to ensure reproducibility:

* Operating System
* Python version
* Library versions
* CPU configuration
* GPU configuration
* Memory information
* Docker image version

## Benefits of Experiment Tracking

* Reproducible machine learning experiments
* Easy comparison between model versions
* Faster debugging and troubleshooting
* Better collaboration among teams
* Improved model governance and auditability
* Simplified model deployment decisions

## Popular Experiment Tracking Tools

* MLflow
* Weights & Biases (W&B)
* Neptune.ai
* Comet ML
* TensorBoard

## Typical Workflow

1. Start a new experiment.
2. Log parameters and dataset version.
3. Train the model.
4. Record metrics during training.
5. Save model artifacts.
6. Track system information and code version.
7. Compare experiments.
8. Register and deploy the best-performing model.

Experiment tracking is a core component of MLOps and enables teams to build reproducible, scalable, and production-ready machine learning systems.

################################################################################################################################

# MLFLOW

MLflow is an open-source MLOps platform used to manage the complete machine learning lifecycle, including:

Experiment Tracking
Model Versioning
Model Registry
Model Deployment
Reproducibility of ML experiments

It helps data scientists and ML engineers track, compare, and deploy machine learning models efficiently.

### Installation

pip install mlflow
mlflow ui --backend-store-uri sqlite:///mlflow.db --port 7000

#### k8s installation

helm repo add community-charts https://community-charts.github.io/helm-charts
helm repo update
helm install mlflow-community communit-charts/mlflow 
kubectl port-forward po/mlflow-community-7549fbf58-x7vjr 7000:5000 --address 0.0.0.0

for now we are running this mlflows as stateless and in production we statefull 

helm repo add bitnami https://charts.bitnami.com/bitnami

helm install postgres bitnami/postgresql
kubectl get secret --namespace default postgres-postgresql -o jsonpath="{.data.postgres-password}" | base64 -d 
VNKK9cBZP1mX0s0upqpAcomy
kubectl exec -it postgres-postgresql-0 -- bash
psql -U postgres
\l --> to check db
CREATE DATABASE mlflow;
CREATE USER mlflow_user WITH PASSWORD 'test123';
GRANT ALL PRIVILEGES ON DATABASE mlflow TO mlflow_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO mlflow_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO mlflow_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO mlflow_user;
ALTER SCHEMA public OWNER TO mlflow_user;
GRANT CREATE ON SCHEMA public TO mlflow_user;

helm install minio bitnami/minio

mlflow server \
--backend-store-uri postgresql://user:password@postgres:5432/mlflow \
--default-artifact-root s3://mlflow-artifacts \
--host 0.0.0.0


helm install mlflow-community community-charts/mlflow \
--set backendStore.databaseMigration=true \
--set backendStore.postgres.enabled=true \
--set backendStore.postgres.host=postgres-postgresql.default.svc.cluster.local \
--set backendStore.postgres.port=5432 \
--set backendStore.postgres.database=mlflow \
--set backendStore.postgres.user=mlflow_user \
--set backendStore.postgres.password=test123

kubectl port-forward po/mlflow-community-7549fbf58-x7vjr 7006:5000 --address 0.0.0.0

#######################################################################################################

# Popular ways to deploy and serve models

1. REST API Serving
Deploy models behind REST APIs.
Common tools:
FastAPI
Flask
Django
Best for custom inference logic.

2. Kubernetes-Native Serving
Scalable and production-ready deployments on Kubernetes.
Common tools:
KServe
Seldon Core
Knative
Supports autoscaling, canary deployments, and A/B testing.

3. MLflow Model Serving
Deploy models directly from the MLflow registry.
Tool:
MLflow
Useful for quick deployments and model management.

4. Cloud Managed Services
Fully managed inference endpoints.
Examples:
Amazon SageMaker
Google Vertex AI
Azure Machine Learning

5. High-Performance Model Servers
Optimized for low latency and high throughput.
Examples:
NVIDIA Triton Inference Server
TensorFlow Serving
TorchServe

6. Batch Inference
Run predictions on large datasets periodically.
Commonly implemented using:
Kubernetes Jobs
Apache Spark
Airflow DAGs
AWS Batch

7. Serverless Inference
Pay only when requests arrive.
Examples:
AWS Lambda
Knative Serving
Cloud Functions

############################################################################################################

### We can use wsgi for our app.py with below cmd

gunicorn --workers 3 --bind 127.0.0.1:6000 wsgi:app

#############################################################################################################

## KServe Model Serving

### Overview

This project demonstrates how to deploy and serve Machine Learning models on Kubernetes using KServe. KServe is a Kubernetes-native model serving platform that provides serverless inference, automatic scaling, canary deployments, and support for multiple ML frameworks.

### Features

* Kubernetes-native model serving
* Automatic scaling (including scale-to-zero)
* Support for TensorFlow, PyTorch, Scikit-learn, XGBoost, and ONNX models
* REST-based inference APIs
* Canary deployments and traffic splitting
* Integration with Kubernetes observability tools

### Prerequisites

* Kubernetes Cluster
* kubectl
* KServe installed
* Knative Serving
* Container Registry (optional)
* Object Storage (S3, MinIO, GCS, etc.)

### Deployment

Apply the InferenceService manifest:

```bash
kubectl apply -f inference-service.yaml
```

Verify deployment:

```bash
kubectl get inferenceservice
```

### Sample Inference Request

```bash
curl -X POST http://<MODEL_ENDPOINT>/v1/models/model:predict \
-H "Content-Type: application/json" \
-d '{"instances":[[1,2,3,4]]}'
```

### Project Structure

```text
.
├── manifests/
│   └── inference-service.yaml
├── models/
├── scripts/
└── README.md
```

### Monitoring

Monitor model serving metrics using Prometheus, Grafana, or SigNoz.

### References

* KServe Documentation
* Kubernetes Documentation
* Knative Documentation

### License

This project is licensed under the MIT License.

##################################################################################################

# Amazon SageMaker AI

## Overview

Amazon SageMaker AI is a fully managed Machine Learning (ML) service provided by AWS that enables developers and data scientists to build, train, deploy, and monitor machine learning models at scale. It simplifies the end-to-end ML lifecycle by providing integrated tools for data preparation, model training, deployment, inference, and monitoring.

## Key Features

* Fully managed machine learning platform
* Built-in algorithms and pre-trained models
* Distributed training support
* Real-time and batch inference
* Automated model tuning (Hyperparameter Optimization)
* MLOps capabilities with CI/CD integration
* Model monitoring and drift detection
* Seamless integration with AWS services such as S3, IAM, CloudWatch, and ECR

## Architecture

```text
Data Sources
      │
      ▼
 Amazon S3
      │
      ▼
 SageMaker Training Jobs
      │
      ▼
 Trained Model Artifacts
      │
      ▼
 SageMaker Endpoint
      │
      ▼
 Prediction Requests
```

## Components

### SageMaker Studio

A web-based integrated development environment (IDE) for machine learning development, experimentation, and deployment.

### Training Jobs

Train machine learning models using managed infrastructure with support for CPU and GPU workloads.

### Model Registry

Centralized repository for managing, versioning, and approving machine learning models.

### Endpoints

Deploy models for real-time inference with automatic scaling and high availability.

### Batch Transform

Run large-scale offline inference on datasets stored in Amazon S3.

### Model Monitor

Continuously monitor deployed models for data quality issues and prediction drift.

## Benefits

* Accelerates machine learning development
* Reduces infrastructure management overhead
* Supports enterprise-grade security and compliance
* Enables scalable model deployment and monitoring
* Integrates seamlessly with AWS cloud services

## Use Cases

* Natural Language Processing (NLP)
* Recommendation Systems
* Fraud Detection
* Computer Vision
* Predictive Analytics
* Customer Churn Prediction

## References

* AWS SageMaker Documentation
* AWS Machine Learning Services Documentation

## License

This project is licensed under the MIT License.

######################################################################################################

# Kubeflow

## Overview

Kubeflow is an open-source Machine Learning (ML) platform built on Kubernetes that simplifies the deployment, orchestration, and management of machine learning workflows. It provides a comprehensive set of tools for developing, training, tuning, serving, and monitoring machine learning models in a cloud-native environment.

Kubeflow enables data scientists and ML engineers to leverage Kubernetes for scalable and reproducible machine learning operations (MLOps).

## Key Features

* **Kubeflow Pipelines** - Build and automate end-to-end ML workflows.
* **Jupyter Notebooks** - Run and manage notebook environments directly on Kubernetes.
* **Katib** - Automated hyperparameter tuning and experiment management.
* **Training Operators** - Distributed training support for TensorFlow, PyTorch, XGBoost, MPI, and more.
* **KServe Integration** - Deploy and serve machine learning and generative AI models at scale.
* **Model Monitoring** - Observe model performance and lifecycle in production.
* **Multi-user Support** - Secure and isolated environments for teams.

## Kubeflow Architecture

```text
Data Ingestion
      ↓
Data Processing
      ↓
Model Training
      ↓
Hyperparameter Tuning
      ↓
Model Registry
      ↓
KServe Model Serving
      ↓
Inference
```

## Core Components

| Component          | Purpose                                 |
| ------------------ | --------------------------------------- |
| Kubeflow Pipelines | Workflow orchestration for ML pipelines |
| Jupyter Notebooks  | Interactive development environment     |
| Katib              | Hyperparameter tuning                   |
| Training Operators | Distributed model training              |
| KServe             | Model serving and inference             |
| Central Dashboard  | Unified user interface                  |

## Kubeflow and KServe

KServe is a core model serving component commonly used within the Kubeflow ecosystem. While Kubeflow manages the complete machine learning lifecycle, KServe focuses specifically on deploying and serving machine learning models on Kubernetes.

```text
Kubeflow
 ├── Notebooks
 ├── Pipelines
 ├── Katib
 ├── Training Operators
 └── KServe
        ↓
     Model Serving
```

## Benefits

* Kubernetes-native ML platform
* Scalable and reproducible ML workflows
* Simplified model deployment and serving
* Automated training and tuning
* Support for MLOps best practices
* Integration with cloud-native tooling

## Use Cases

* End-to-end MLOps platforms
* Model training and experimentation
* Hyperparameter optimization
* Batch and real-time inference
* Generative AI and LLM deployment
* Enterprise machine learning workflows







