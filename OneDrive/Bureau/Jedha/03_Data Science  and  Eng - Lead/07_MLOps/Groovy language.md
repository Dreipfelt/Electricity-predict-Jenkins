CICD
Groovy Language 👯
30 min
What you will learn in this course 🧐🧐

In this course, you will dive into the fundamentals of Groovy scripting in the context of Jenkins pipelines. Groovy is the scripting language used to define and automate Jenkins pipelines, allowing for powerful, flexible, and reusable CI/CD workflows. By the end of this session, you will:

    Understand the basics of Groovy and its syntax.
    Learn how Groovy is integrated into Jenkins for defining pipelines.
    Explore how to write and manage Jenkins Declarative and Scripted pipelines using Groovy.
    Understand key Groovy constructs such as variables, methods, closures, and classes in the context of Jenkins pipelines.
    Implement practical examples of Groovy within Jenkins pipelines, including conditional logic, loops, and error handling.

What is Groovy?
1. Groovy Overview

Groovy is an agile, dynamic language for the Java platform that can be used as both a scripting language and for writing applications. It offers a syntax that’s very similar to Java but with additional features to simplify common tasks. In Jenkins, Groovy is the core language used to define both declarative and scripted pipelines.
2. Why Groovy in Jenkins?

Jenkins Pipelines are written as code using Groovy, enabling automation of various stages in a CI/CD pipeline. Groovy is tightly integrated with Jenkins, and its dynamic nature makes it ideal for scripting complex logic into your pipelines, such as:

    Handling conditional build logic.
    Performing loops for repeated steps.
    Defining reusable functions and pipeline libraries.
    Error handling and debugging pipeline stages.

Declarative vs Scripted Pipelines

Before diving into Groovy syntax, it’s essential to understand the two types of Jenkins pipelines: Declarative and Scripted.
1. Declarative Pipeline

The Declarative Pipeline provides a simpler, more structured way to define your pipeline using a pre-defined, structured syntax. It is recommended for most users because it makes pipeline creation more accessible and readable.

Example:

pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Building...'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying...'
            }
        }
    }
}

2. Scripted Pipeline

The Scripted Pipeline is a more flexible pipeline type based entirely on Groovy. It allows for more complex control over the pipeline steps, making it suitable for advanced users with custom requirements.

Example:

node {
    stage('Build') {
        echo 'Building...'
    }
    stage('Test') {
        echo 'Testing...'
    }
    stage('Deploy') {
        echo 'Deploying...'
    }
}

Groovy Basics for Jenkins Pipelines

Now that you understand the two types of pipelines, let's explore Groovy syntax and constructs as applied to Jenkins pipelines.
1. Variables

In Groovy, variables can be declared dynamically. They can store different data types (e.g., strings, integers, booleans).

Example:

def name = "Jenkins"
def buildNumber = 123
def isSuccess = true

You can use variables in your pipeline to pass data between stages:

pipeline {
    agent any
    stages {
        stage('Echo Variables') {
            steps {
                script {
                    def name = "Jenkins Pipeline"
                    echo "Project Name: ${name}"
                }
            }
        }
    }
}

2. Conditions

Conditional logic allows your pipeline to make decisions during execution. Groovy supports if-else statements as well as switch-case for conditional execution.

Example of if-else:

pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                script {
                    def buildStatus = "success"
                    if (buildStatus == "success") {
                        echo "Build passed"
                    } else {
                        echo "Build failed"
                    }
                }
            }
        }
    }
}

Example of switch-case:

pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                script {
                    def buildType = "debug"
                    switch(buildType) {
                        case "debug":
                            echo "Building in debug mode"
                            break
                        case "release":
                            echo "Building in release mode"
                            break
                        default:
                            echo "Unknown build type"
                    }
                }
            }
        }
    }
}

3. Loops

Loops in Groovy are essential for repetitive tasks. You can use for, while, and each loops to iterate over collections.

Example of for loop:

pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                script {
                    for (int i = 1; i <= 3; i++) {
                        echo "Iteration: ${i}"
                    }
                }
            }
        }
    }
}

Example of each loop (for collections):

pipeline {
    agent any
    stages {
        stage('Deploy') {
            steps {
                script {
                    def servers = ['Server1', 'Server2', 'Server3']
                    servers.each { server ->
                        echo "Deploying to ${server}"
                    }
                }
            }
        }
    }
}

4. Functions (Methods)

In Groovy, functions (or methods) can be used to encapsulate reusable code. This is useful for modularity and readability in your pipeline scripts.

Example:

def greet(name) {
    echo "Hello, ${name}"
}

pipeline {
    agent any
    stages {
        stage('Greet') {
            steps {
                script {
                    greet('Jenkins User')
                }
            }
        }
    }
}

5. Error Handling

Groovy supports robust error handling using try-catch blocks. This is crucial in Jenkins pipelines to handle failures gracefully.

Example:

pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                script {
                    try {
                        // Simulate build step
                        echo 'Building...'
                        error 'Build failed!'
                    } catch (Exception e) {
                        echo "Caught error: ${e.message}"
                    }
                }
            }
        }
    }
}

Advanced Groovy Constructs in Jenkins Pipelines
1. Groovy Closures

Closures are anonymous blocks of code that can be assigned to variables and passed as parameters to methods.

Example:

def greet = { name -> 
    echo "Hello, ${name}"
}

pipeline {
    agent any
    stages {
        stage('Greet') {
            steps {
                script {
                    greet('Groovy Developer')
                }
            }
        }
    }
}

2. Shared Libraries

Jenkins allows you to create reusable pipeline code through shared libraries. This enables you to share common Groovy functions or classes across multiple pipelines.

Defining a Shared Library:

    Create a vars folder in the shared library repository.
    Inside the vars folder, create Groovy scripts with reusable functions.

Example of a Shared Library Function (greeting.groovy):

def call(String name = 'World') {
    echo "Hello, ${name}"
}

Using the Shared Library in a Jenkinsfile:

@Library('my-shared-library') _

pipeline {
    agent any
    stages {
        stage('Greet') {
            steps {
                greeting('Jenkins User')
            }
        }
    }
}

Integrating Groovy into Jenkins Pipelines
1. Groovy and Jenkinsfile

The Jenkinsfile is where your Groovy code lives. Whether you're using a Declarative or Scripted pipeline, Groovy controls the flow of your pipeline's logic.
2. Common Groovy Use Cases in Pipelines

    Automating repetitive tasks (e.g., building multiple projects or deploying to multiple environments).
    Pipeline branching logic based on different conditions (e.g., deploying only if certain tests pass).
    Modularizing the pipeline into reusable stages or methods.

3. Integrating Groovy with CI Pipelines

Once you've mastered Groovy basics, you can integrate your pipelines with CI tools like Jenkins. Use Groovy for:

    Defining pipeline stages for building, testing, and deploying applications.
    Automating unit testing with tools like JUnit.
    Managing deployment logic across multiple servers.

Resources 📚📚

    Groovy Documentation
    Jenkins Pipeline Syntax
    Jenkins Declarative Pipeline
    Jenkins Scripted Pipeline
    Groovy Closures
    Shared Libraries in Jenkins
