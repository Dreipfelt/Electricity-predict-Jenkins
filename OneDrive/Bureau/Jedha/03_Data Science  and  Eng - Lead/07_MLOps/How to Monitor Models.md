Continuous Monitoring
How to Monitor Models 👩‍🔬
15 min
What you will learn in this course 🧐🧐

You wipe your forehead, proud of you've accomplished because after months of hard work, you have finally put your AI model into production! The world looks bright to you. What could go wrong?

Everything! 😈

Monitoring system is a very important part of maintaining a sustainable product following the long-terms requirements. There are several threats for machine learning in production. We are going to see how to protect ourselves from those threats by covering the following topics:

    What is monitoring?
    Monitoring in ML world
    Model threats

What is monitoring?

Monitoring is the process of observing the state of a system.

As systems are getting more and more complex, they become more prone to errors. ML models are not exempt from this kind of entropic behavior. Models performance tend to indeed decrease over time because of several factors:

    Data can change from the training dataset
    Execution environment (machines) is less efficient
    ...

All this make it very important to know when an ML Model's performance start decreasing. Especially when your business relies machine learning to run properly.

In common application development, it is essential to watch how your code and architecture are doing in real environment. Logging appears to be a good way to monitor system. Watching metrics, such as CPU usage, or pages requests, are good proxies on application health in order to maintain a good service.

The same goes for machine learing projects. Monitoring is a crucial tool to understand your model in production. It alerts you when something goes wrong or how you could improve predictions. In other words, monitoring guarantees that your model is working as expected.
Monitoring in ML world

Monitoring is great to keep an eye on production. But how to proceed?

There aren't one size fits all solutions. But most of the time you rely on a model in production inside an specific environment (server, OS, packages and so on). Most of the time this model is requestable through an API, certainly a REST API.

So your users will request your model and will get a response. You can simply log these requests and responses. Those logs can be stored in files on S3, or locally, or in a database. It all depends on your needs.

Monitoring basic

Monitoring relies on this precious data. You are free to log and monitor any metric you want.

It is indeed common to monitor not only ML model specific metrics, but also other metrics like CPU usage, memory usage, network usage, etc., so called the service health, in order to avoid technical issues.

Monitoring KPIs also will help you to understand how a model is helping to reach business goals for example.

Another aspect of monitoring is the data quality check. If you are able to check that data is in good shape to pass through your model then it is easier to avoid errors.
Model threats

Now that you have a broader idea of what is monitoring, let's discuss the main reasons why a model's performance can decrease. We call this phenomenon: model decay and one of the main reason why decay happens is because of drift which is the idea that there is a change from the initial experiment environment to the new "real-life" environment.

Drift can happen in 3 different ways:

    The gradual drift, is the common one. Things changes with time and the data is affected by those changes.
    The sudden drift happens when someting brutal changes, like the COVID crisis.
    The recurring drift is just the effect of the seasonality on data.

The most common issue for ML models in production are data and target drift.

Drift visual

Source
Data drift

Data drift, or covariate shift, is the fact that the input data in production is less and less representative of the one in your training set. In other term, the distribution of the input data has changed.

This can come from various reasons:

    world events (COVID),
    applying the model in a different context,
    the training set was biased,
    and so on.

Data drift happens often and it is more a matter of when rather than if it will happen. The only thing is to set a threshold after which we consider that data has drifted too much.
NOTE

There is also another type of drift which affects the target variable (target variable distribution is not the same as in the training set for example) that you might hear about. Although it definitely exists, it affects less ML model in general.
Target drift

The target drift (or concept drift) happens when the input data and the output variable lost their relations. The model is no more representative of what happens in reality.
Other

Drift is not the only threat for our models. We can also monitor outliers and the related topic the adversarial attacks where some people may take advantages of the model biases.
Resources 📚📚

    The paper that consecrated MLOps: Hidden Technical Debt in Machine Learning Systems
    Monitoring and explainability of models in production
    Notes on data distribution shifts and monitoring
