# Building a RESTful API for Similarity Check using Natural Language Processing

## Overview
This project implements a RESTful API for comparing the similarity between two texts using Natural Language Processing (NLP) techniques. It leverages SpaCy for NLP tasks and MongoDB for data storage.

## Features
- **User Registration and Authentication**: Allows users to register, authenticate, and manage tokens for API usage.
- **Text Similarity Calculation**: Computes the similarity score between two texts using SpaCy's NLP capabilities.
- **Admin Functions**: Includes administrative functions for user management and token refilling.

## Technologies Used
- Python
- Flask
- Flask-RESTful
- SpaCy
- MongoDB
- Docker
- Gunicorn

## File Structure
```
application_1/
├── db/
│ └── Dockerfile
├── web/
│ ├── app.py
│ ├── Dockerfile
│ ├── requirements.txt
│ ├── en_core_web_sm-2.0.0.tar.gz <-- Your model file
└── docker-compose.yml

```

** Download SpaCy Model
Download the SpaCy model en_core_web_sm from the following link: https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.0.0/en_core_web_sm-2.0.0.tar.gz

**after download, put the model inside web folder ".

** Build and run the Docker Image:
Open a terminal and navigate to the application_1 directory. Build the Docker image using the command "docker build" and then run the command "docker up".


##API Endpoints:
-POST /register: Register a new user.
-POST /admin: Register a new admin.
-POST /detect: Compare similarity between two texts.
-POST /refill: Refill tokens for a specified user.


##Usage Examples:


-User Registration:
```
{
  "username": "example_user",
  "password": "password"
}
```

-Admin Registration:
```
{
  "username": "admin_user",
  "password": "admin_password"
}

```

-Token Refill:
```
{
  "username": "example_user",
  "refilled user": "your_admin_key",
  "amount": 100  // Number of tokens to refill
}
```
