Continuous Monitoring
Monitoring DAG 🔄
75 min
What you will learn in this course 🧐🧐

For this last course, we want to demonstrate how to integrate monitoring in your MLOps pipeline. To do so, we will be build a sample DAG in airlfow that integrates evidently.
Demo setup

If you want to follow along 👇

git clone https://github.com/JedhaBootcamp/sample-evidently-dag.git

This is an airflow code That tries to detect data drift.
IMPORTANT

🚨 ONE THING THAT YOU NEED TO MAKE SURE IS TO ADD THE ENVIRONMENT VARIABLE IN THE AIRFLOW VARIABLES (Admins > Variables) 🚨 You have EVIDENTLY_CLOUD_TOKEN & EVIDENTLY_CLOUD_PROJECT_ID.

Check out yesterday's tutorials if you don't remember how to do it.

Don't freak out if you see an error when opening Airflow for the first time. The most likely reason is because of the above 😉
The code

What should this DAG do? Here is an overview:

Final DAG

It should observe a file in the ./data/data-drift folder and if one file is put inside, it should compute the data drift between the current data and a reference sample.

If data drift is detected, a report is sent back to your Evidently Cloud account to inform the data science team about data drift. If no data drift is detected, it should do nothing special.

You will find in the data folder:

    reference/weather-reference-sample.csv: the reference data took from the training set,
    data-drift/week1.csv: a first sample took during the first week of february,
    data-drift/week2.csv: a second sample took during the first week of february,
    data-drift/week3.csv: a third sample took during the first week of february,

Other important files to read are:

    docker-compose.yaml, Dockerfile and requirements.txt: that setups up your environment

NOTE
|
Airflow environment

The whole environment is meant to run locally using docker compose up -d to simplify the whole demo. But if you want to use your Airflow server from HuggingFace Space in the previous tutorials, you definitely can.

Also docker-compose.yaml shows several containers. In this development environment, we seperated each part of Airflow application into seperate containers. That is why you will see:

    One container for the Web Application
    One container for the Worker
    One container for the Scheduler
    One container for the PostgreSQL DB
    One container for the Redis DB (meant to store application data compared to the PostgreSQL only meant to store DAG data)

💡 If you want to troubleshoot your code, the containers you will most likely need to debug first will be the web app or the worker container.

Let's now break down the code task-by-task:
detect_file

This task is a sensor operator. We use the PythonSensor to monitor any changes in the data-drift folder.

If any files looking like week*.csv (the * could be any character), then the rest of the DAG process is triggered (functions returns True), otherwise it waits (function returns False).
detect_data_drift

This is the actual task where you are computing whether there is data drift or not using evidently. You should use the BranchPythonOperator in order to create a conditional branching.

If data drift is detected then the next task in the DAG will be data_drift_detected, otherwise the next task will be no_data_drift_detected.
data_drift_detected

This tasks run a report and export it to the Evidently cloud project of your choice. This depends on what you inserted in the environment variables at the beginning. This is a great way to share to other team members and plan accordingly.
no_data_drift_detected

We used a simple DummyOperator that basically doesn't do anything. However if you want to use fork that repo and build up on it, you can check out something harder to do 😉
clean_file

We optionally wrote a function that will erase the last file added in ./data/data-drift. It's not part of the default DAG but if you were to use something like this in production you would want to use it as you will need to free up some space on the container at some point.

Happy coding! 🚀
Resources 📚📚

    Sample Evidently DAG
    DAGs
