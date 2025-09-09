Continuous Training
Jenkins Server & ML App 👩‍🔬
60 min
What you will learn in this course 🧐🧐

Now the MLflow server is up and running, we are going to setup Jenkins to handle the testing phase of our project. While we are at it, we will also give you the Machine Learning client (i.e the actual application) that will be tested and staged to production. Without further ado, let's get to it 💪
Demo setup

Here are useful links if you want to follow along with the demo below:

    Sample Jenkins Server - Github repo
    Sample ML Workflow (The actual application) - Github Repo
    Ngrok 👉 You will need to create an account
    AWS

✅ Jenkins Setup Walkthrough (Local with Proxy Access)
🧭 Goal

Set up a Jenkins server locally using Docker Compose, and expose it to the web using ngrok, to simulate a semi-production environment.
Step 1: Clone the Jenkins Repository

Follow the installation tutorial from the CICD day to setup Jenkins.

Access Jenkins at:

http://localhost:8080

Step 2: Install and Set Up ngrok

    To make your local Jenkins server accessible from the internet.

    Go to https://ngrok.com.

    Sign up and verify your email.

    Install ngrok:

        macOS:

        brew install ngrok

Windows (via Choco):

choco install ngrok

Linux:

sudo snap install ngrok

Docker alternative:

docker pull ngrok/ngrok

Step 5: Authenticate ngrok

    Find your authtoken in your ngrok dashboard.

    Add it using:

    ngrok config add-authtoken <your-token>

Step 6: Start a Tunnel to Jenkins

    Forward external traffic to Jenkins running locally on port 8080:

    ngrok http http://localhost:8080

    Copy the public URL provided (e.g., https://abcd-1234.ngrok.io).

    Open it in your browser — you should now see your Jenkins dashboard online.

✅ Result

You now have:

    A fully functioning Jenkins server running locally.
    Web access via a secure URL (using ngrok).

📝 Notes

    Do NOT reuse tokens shown in demos — they are deactivated after recording.
    This method is ideal for local testing, demos, or when Hugging Face/AWS setups are not working.

✅ Step-by-Step: Running ML Pipeline with Jenkins and MLflow
🎯 Goal:

Set up a Jenkins pipeline to automate the training of an ML model using MLflow, with credentials injected via environment variables.
🧩 Step 1: Clone the Sample ML Workflow

    Go to the JLA Bootcamp GitHub account.

    Search for: sample-ml-workflow.

    Clone the repository:

    git clone https://github.com/JedhaBootcamp/sample-ml-workflow.git
    cd sample-ml-workflow

🧠 Step 2: Understand the Code Structure

    Model Training Logic:

        Uses Scikit-Learn to:
            Load & preprocess data.
            Split into train/test.
            Scale data using StandardScaler.
            Train using RandomForestRegressor with a grid search.

    Experiment Logging:
        Metrics and models are logged using MLflow.
        mlflow.sklearn.autolog() is used for convenience.

    Data Source:
        California housing dataset from an S3 bucket.

    Hyperparameter Grid:

    {
      'regressor__n_estimators': [90, 100],
      'regressor__criterion': ['squared_error']
    }

    Other Important Files:
        Dockerfile: Defines environment for ML pipeline.
        MLproject: Enables remote MLflow execution.
        Jenkinsfile: Defines the CI/CD steps in Groovy.

🧪 Step 3: Understand the Test Coverage

The repo includes simple test cases to:

    Check if data loads.
    Confirm preprocessing and train/test split works.
    Validate model training executes without error.

🐳 Step 4: Understand Jenkinsfile Logic

This CI/CD pipeline will:

    Clone the repository.
    Build a Docker image.
    Inject environment variables (credentials).
    Run the ML workflow inside Docker.
    Clean up the Docker environment.

🔐 Step 5: Set Up Jenkins Credentials

    Required before running the pipeline!

    In Jenkins:
        Go to Manage Jenkins → Credentials → System → Global Credentials.
        Click “Add Credentials”.

    For each required secret:

        Choose “Secret Text”.

        Paste the secret value (e.g., AWS Access Key).

        Use the ID exactly as referenced in the Jenkinsfile. Example:
            ID: aws-access-key
            Description: aws-access-key

    Repeat for all required secrets:
        mlflow-tracking-uri: the uri of your mlflow tracking server hosted on hugginf face
        aws-access-key: the aws access key id provided by aws
        aws-secret-key: the aws secret access key if provided by aws
        backend-store-uri: the connection string provided by neon db
        artifact-root: the s3 uri of your bucket (in the form s3://your-bucket-name)

🏗️ Step 6: Create a Jenkins Pipeline Job

    Go to Jenkins → New Item.

    Name it: grid-search-demo.

    Choose Pipeline → Click OK.

    Configure:

        Description: "Demo hyperparameter tuning job".

        Build Triggers:
            Enable Poll SCM: H/20 * * * * (every 20 minutes).

        Pipeline Script From SCM:
            SCM: Git.
            Repository URL: https://github.com/JedhaBootcamp/sample-ml-workflow
            Branch: main.
            Script path: Jenkinsfile.

🚀 Step 7: Run the Jenkins Job

    Return to the dashboard.

    Click Build Now to start the pipeline manually.

    Click the running job → Console Output.

    You should see:
        Docker image build
        Dependency installation
        Model training
        Successful test runs
        Cleanup
        Success message

✅ Final Outcome

You now have a Jenkins-powered CI/CD workflow that:

    Pulls the latest ML code
    Injects secrets securely
    Builds a Docker environment
    Runs and tracks experiments via MLflow
    Cleans up automatically

Resources 📚📚

    Jenkins
    Ngrok

    What you will learn in this course 🧐🧐
    Demo setup
    ✅ Jenkins Setup Walkthrough (Local with Proxy Access)
    ✅ Step-by-Step: Running ML Pipeline with Jenkins and MLflow
    Resources 📚📚

Skip
Validate👍
Logo Jedha Footer