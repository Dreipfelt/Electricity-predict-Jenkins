Continuous Training
Mlflow Server 🔄
30 min
What you will learn in this course 🧐🧐

Mlflow is one of the greatest tool for MLOps for model reproducibility. While this course doesn't cover MLflow's functionality, we want to show you how to stage it into production for free using HuggingFace Spaces.
Demo setup

Here are useful links if you want to follow along with the demo below:

    MLflow server Github repo
    PostgreSQL with Neon 👉 You will need to create an account
    HuggingFace Spaces 👉 You will need to create an account
    AWS 👉 You will need to create an account

🧭 Walkthrough: Deploying an MLflow Server to Production Using Hugging Face Spaces
🎯 Objective

In this walkthrough, you will deploy an MLflow server on Hugging Face Spaces using a Docker container. This is the first step toward setting up a full MLOps pipeline for continuous training and model management.
🛠️ Prerequisites

Before you begin, make sure you have the following:

    A Hugging Face account (create one at huggingface.co if needed)
    Git installed on your machine
    A code editor (e.g., VS Code)
    Basic familiarity with Git, Docker, and the terminal

📦 Step 1: Clone the MLflow Server Template from GitHub

The Jedha Bootcamp GitHub has a ready-to-use template for deploying MLflow on Hugging Face.

    Navigate to the Jedha Bootcamp GitHub repository
    Look for the repository named mlflow-server-on-huggingface
    Copy the HTTPS clone URL from the "Code" button
    Open your terminal and run:

cd ~/Desktop  # or any directory of your choice
git clone https://github.com/JedhaBootcamp/mlflow-server-on-hugging-face.git
cd mlflow-server-on-huggingface

    Open the repo in VS Code:

code .

🔍 Step 2: Inspect the Dockerfile

The Dockerfile you'll find is tailored for Hugging Face Spaces. It starts from a miniconda base image and installs a few essential tools (like AWS CLI) before launching the MLflow server.

No need to modify anything for now — we’ll use this as-is.
🚀 Step 3: Create a New Hugging Face Space

    Go to https://huggingface.co and sign in

    Click on your profile picture (top right) → "New Space"

    Fill in the space creation form:
        Name: mlflow-server-demo
        License: Apache 2.0 (default is fine)
        SDK: Select Docker
        Hardware: Choose the free tier (2 vCPUs, 16GB RAM)
        Visibility: Public (important for later use in Airflow and API access)

    Click "Create Space"

You’ll be redirected to a GitHub-like page for your space.
🌐 Step 4: Link Your Local Repo to the Hugging Face Space

    Copy the Git URL of your Hugging Face space (e.g., https://huggingface.co/spaces/yourname/mlflow-server-demo)
    In your terminal, add it as a remote:

git remote add hf https://huggingface.co/spaces/yourname/mlflow-server-demo

    Confirm remotes:

git remote -v

You should see both origin (GitHub) and hf (Hugging Face).
🔄 Step 5: Handle the README Merge Conflict

Hugging Face automatically creates a README.md in your new space, which might cause a merge conflict when pushing. Let’s fix that:

git pull hf main --rebase

If there's a conflict:

    Open README.md in your editor
    Accept "Current Changes" (i.e., keep the Hugging Face version)
    Then run:

git add README.md
git commit -m "Resolve README conflict with HF"
git rebase --continue

Repeat if needed until the rebase completes.
⬆️ Step 6: Push to Hugging Face and Trigger the Build

Now you’re ready to push your code to the Hugging Face space:

git push hf main

Once the code is pushed, Hugging Face will automatically build the Docker image and attempt to launch the container.
🧪 Step 7: Observe the Build and Debug Errors (if any)

After a few moments, Hugging Face will show the build logs.

    ⚠️ You might see an error like invalid value for port. That’s expected!

This happens because we haven’t set all the required environment variables yet (those will be added in the next walkthrough).
✅ What You Accomplished

You’ve now:

    Cloned and understood a Dockerized MLflow server
    Created a space on Hugging Face to run MLflow in production
    Handled Git remotes and merge conflicts
    Triggered your first Hugging Face Docker build

Your MLflow server is almost ready to serve models—just a few more configuration steps remain.
🔜 What’s Next?

In the next walkthrough, you'll:

    Set up required environment variables for MLflow to run correctly
    Finalize the deployment and test that your MLflow UI is working in the Hugging Face space

Stay sharp, and remember—you’re building real MLOps infrastructure step by step.
🧭 Walkthrough: Configuring Environment Variables for MLflow on Hugging Face Spaces
🎯 Goal

By the end of this walkthrough, you will have:

    Set up secure environment variables to connect MLflow with AWS (S3) and PostgreSQL (via Neon.tech)
    Successfully restarted your Hugging Face Space to activate your MLflow server
    Learned how to access the actual MLflow UI endpoint

🛠️ Step 1: Create AWS Credentials
1.1 Log into AWS and Open IAM

    Go to https://console.aws.amazon.com
    Navigate to IAM (Identity and Access Management)

1.2 Create a New User

    Click "Create User"
    Name the user (e.g., mlflow-user-demo)
    Assign **** (✅ fine for testing, ⚠️ not for production)
    Create the user and go to their Security credentials

1.3 Generate Access Keys

    Scroll to Access Keys → Click Create access key

    Choose CLI as the use case

    Download the .csv file containing:
        AWS_ACCESS_KEY_ID
        AWS_SECRET_ACCESS_KEY

✅ Important: Save the .csv file securely — AWS only shows this once.
🗃 Step 2: Create an S3 Bucket for Artifact Storage
2.1 Navigate to S3

    In AWS, go to S3
    Click "Create bucket"

2.2 Bucket Setup

    Name it something like: mlflow-artifacts-demo-1234 no uppercase letters or underscores

2.3 Copy S3 URI

    If the “Copy URI” button is grayed out, start a fake upload
    You'll see a URI like: s3://mlflow-artifacts-demo-1234
    Save this URI — this is your ARTIFACT_STORE_URI

🧾 Step 3: Prepare Environment Variables Locally

Inside your mlflow-server-on-huggingface repo, create a file called secrets.sh:

# secrets.sh

AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
ARTIFACT_STORE_URI=s3://mlflow-artifacts-demo-1234

You’ll complete it in the next step.
🛢 Step 4: Create a Free PostgreSQL Database (Backend Store)
4.1 Sign Up on Neon.tech

    Go to https://neon.tech and sign up
    Once verified, go to your dashboard

4.2 Create a Project

    Click “Create Project” → Choose a name
    The free plan gives you 1 project with a PostgreSQL database

4.3 Copy Connection URI

    In your project, find the PostgreSQL connection string
    It looks like: postgresql://user:password@hostname/dbname

Add this to your secrets.sh:

BACKEND_STORE_URI=postgresql://user:password@hostname/dbname

🌐 Step 5: Set the Port for Hugging Face

Hugging Face Spaces uses port 7860 for custom Docker apps. Add it to your secrets.sh:

PORT=7860

✅ Now your full secrets.sh should look like this:

AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
ARTIFACT_STORE_URI=s3://mlflow-artifacts-demo-1234
BACKEND_STORE_URI=postgresql://user:password@hostname/dbname
PORT=7860

🔒 Step 6: Add Secrets in Hugging Face Space
6.1 Go to Your Space Settings

    Navigate to your MLflow space (e.g., https://huggingface.co/spaces/yourname/mlflow-server-demo)
    Click "Settings" → Scroll to "Secrets and Variables"

6.2 Add Secrets One by One

Click “New secret” and paste each variable from secrets.sh.
Name	Value
AWS_ACCESS_KEY_ID	your AWS access key
AWS_SECRET_ACCESS_KEY	your AWS secret key
ARTIFACT_STORE_URI	your s3://... URI
BACKEND_STORE_URI	your PostgreSQL URI from Neon.tech
PORT	7860

✅ Note: Secrets are private and encrypted — safe for credentials.
🔁 Step 7: Restart the Hugging Face Space

    Go back to the “Files and Versions” tab
    Click “Restart Space”

The Hugging Face platform will rebuild your Docker image and apply the new environment variables.

⏳ Wait ~1–2 minutes.
✅ Step 8: Access the MLflow UI

To see the actual MLflow interface (without Hugging Face branding):

Use this URL pattern:

https://<username>-<space-name>.hf.space

Example:

https://johndoe-mlflow-server-demo.hf.space

This is the URL you’ll use later in Airflow and other MLOps components.
🧹 Optional: Clean Up Previous Experiments

If you reused your database:

    You may see old MLflow runs
    You can click “Delete” on each experiment to reset

🏁 Recap

You now have a fully functional MLflow server running in production, with:

    Secure AWS and PostgreSQL connections
    Proper storage for both metadata and model artifacts
    A clean, dedicated endpoint ready for experimentation

Resources 📚📚

    Getting Started with MLflow
    Spaces Overview
