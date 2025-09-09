Continuous Training
Introduction to Continuous Training 🏃‍♀️
60 min
What you will learn in this course 🧐🧐

With Machine Learning involved, CI/CD concept has evolved and more phases have been added into the mix. One of them is Continuous Training. The idea is pretty simple: Being able to train models automatically.

While CI/CD primarely focus on testing the code and building the environment, CT focuses on launching training jobs regularly based on a given trigger. In this course, we will give you a better idea of what is CT and how to integrate it in Machine Learning workflow.
IMPORTANT
|
Today's course is 100% hands-on demo

All the lectures of today's course will hands-on demo on how to integrate Continuous Training. Technically, you are not going to learn new technologies for this class (especially if you followed the Fullstack program). However, we want to show how to put pieces together in a very advanced way so that you are able to integrate CT.

Make sure to follow all the videos of the following lectures, starting with the one below that will give you some context as of what we will be doing.
🎓 Course Module: Continuous Training in Machine Learning Pipelines
🌟 Learning Objectives

By the end of this module, learners will be able to:

    Define and explain the concept of continuous training in an ML pipeline.
    Understand how continuous training fits into MLOps practices.
    Recognize the technical and operational challenges of retraining models automatically.
    Identify key tools and technologies to orchestrate continuous training (e.g., Jenkins, Airflow, MLflow).
    Design and implement a modular ML pipeline that supports continuous training.

📘 Introduction: Why Continuous Training Matters

In traditional software engineering, CI/CD pipelines automate the building, testing, and deployment of code. In Machine Learning, the need for automation goes further: models can become outdated simply because the data evolves.

This is where continuous training comes in. Instead of manually retraining models each time the data or the code changes, we want to automate the retraining, testing, and deployment of those models so they stay relevant and effective in production.

    💬 Definition (AWS): Continuous training refers to the process where ML systems automatically and continuously retrain models based on triggers such as new data, new code, or performance drift.

🛠️ The Three Stages of the ML Pipeline

Before jumping into automation, let’s revisit the three core stages of any machine learning project:

    Model Development (Local): Work happens in environments like Jupyter or VS Code using frameworks like scikit-learn, PyTorch, or TensorFlow. This is the sandbox where models and feature engineering are tested.

    Model Training (Remote): Once the model code is mature, it's sent to powerful machines—typically cloud-based instances with GPUs (e.g., AWS EC2)—to train on large datasets. This step is expensive and should be reserved for code that is production-ready.

    Model Deployment (Production): After successful training, the model is deployed behind an API (often using FastAPI or MLflow) to serve predictions in real-time environments.

🚨 The Real-World Challenges of Model Training

In industry, a few key concerns arise when moving beyond experimentation:

    Compute costs: Cloud resources (like GPU instances) are billed by the hour. Training models with broken or unoptimized code is wasteful and expensive.
    Model performance regression: Deploying a new model that underperforms compared to the current one can harm business outcomes. We must ensure that only better models make it to production.

✅ The Solution: Test, Orchestrate, Automate

We address the above challenges with two main strategies:
1. Continuous Integration (CI) with Jenkins

Jenkins acts as a "gatekeeper." It runs tests at multiple stages:

    Before training: Ensures the model code is syntactically and functionally correct.
    Before deployment: Evaluates the new model’s performance to ensure it meets (or exceeds) expectations compared to the model already in production.

2. Workflow Orchestration with Airflow

Airflow coordinates the end-to-end flow of the pipeline:

    Detects new training triggers (new data, code changes, or model performance degradation).
    Launches training on remote instances.
    Handles task dependencies (e.g., only deploy if tests pass).

🔁 What Triggers Continuous Training?

Continuous training is activated by three main triggers:

    New Data: As new entries arrive in the data warehouse (e.g., via Airbyte or Airflow ETL jobs), the model may need to be retrained.
    New Features or Code: Changes to preprocessing or the ML algorithm itself.
    Model Drift: If monitoring tools detect performance drop-offs, retraining is automatically scheduled.

🧰 Tools of the Trade: A Full Tech Stack Overview

Let’s connect the dots by looking at the key technologies used at each stage:
Step	Tool	Role
Data Ingestion	Airbyte, Airflow	Populate the data warehouse with new data
Data Warehouse	Snowflake, Redshift, BigQuery	Store and query training data
Experiment Tracking	MLflow	Track model parameters, metrics, artifacts
Training	EC2 (AWS), MLflow Projects	Run scalable training jobs
Testing / CI	Jenkins	Test code and model performance
Orchestration	Airflow	Manage flow from data → training → deployment
Deployment	MLflow Models, FastAPI	Serve model predictions via APIs
Monitoring	Evidently AI	Detect performance issues and trigger retraining
🏗️ The Implementation Blueprint

To build this continuous training pipeline from scratch, here’s the roadmap we’ll follow in upcoming lessons:

    Set up the MLflow server (e.g., using Hugging Face Spaces for a free production-like environment).
    Deploy an Airflow server to orchestrate training triggers and workflow execution.
    Configure reusable training environments using pre-configured EC2 AMIs.
    Build a Jenkins server to run tests at each critical transition point.
    Wire everything together so that new data or performance drops automatically launch model retraining, testing, and deployment.

For local development and server access, we’ll also explore tools like Ngrok, which allows us to expose locally running servers to the web securely—great for quick experiments and testing.
🎯 Conclusion and Why This Matters

Being able to build an automated, production-grade ML pipeline with continuous training is a core competency for any ML engineer or data scientist working at scale.

It ensures your models are always up to date, your deployment process is robust and safe, and your engineering team can focus on what matters: building better models, not babysitting old ones.

    🧠 Think of this as the DevOps revolution—but for data and models. It’s the kind of infrastructure that powers real-world systems in finance, healthcare, e-commerce, and beyond.

🧪 Coming Up Next…

In the next lesson, we’ll start building this pipeline step by step, beginning with setting up your own MLflow server.

Until then, keep in mind: the future of machine learning isn’t just about clever models—it’s about building systems that learn continuously and adapt automatically.

Happy learning!
Resources 📚📚

    MLOps checklist components
