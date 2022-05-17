# THINA AI-App

## Contents

 - [What is this repository for?](#what-is-this-repository-for)
 - [What tecnologies does this project use?](#what-technologies-does-this-project-use)
 - [How do I get set up?](#how-do-i-get-set-up)
 - [Deploy Instructions](#deploy-instructions)
 - [Contribution Guidelines](#contribution-guidelines)
 - [Who do I talk to?](#who-do-i-talk-to)

## What is this repository for?

This repository contains a Web Application that will provide services with important deliverable outputs based on research developed by THINA AI Team. So far we have mapped certain services required to leverage AI proceedings under THINA. They are:

- NER
- Access SNOMED CT 
- (to be added)

## What technologies does this project use?

The application runs an instance of Python's [FastAPI](https://fastapi.tiangolo.com/) framework and its package versioning, dependencies and automation process are delivered by [Poetry](https://python-poetry.org/docs/).

## How do I get set up?

You **will** need Python 3.8 or greater to run this project. A Poetry install is *also* required to install dependencies, but no need to worry: Poetry is combined with a certain script set that will automate certain processes. Consequently, the repo is structured as follows:

```
├── README.md
├── app
│   └── ...
│── scripts
│   ├── __init__.py
│   |── run_app.py
|   └── ...
├── pyproject.toml
└── poetry.lock
```

Following Poetry script guidelines, the folder `scripts` is a package that is intended to automate either the application development itself as well as its deployment stage. So, from within project's folder, in order to run the application in development mode you can run

`poetry install`  

`poetry add --dev poethepoet`  

`poe cuda11`

to install all project dependencies denoted by `pyproject.toml` file. Then run

`poetry run dev`

and head over to `http://127.0.0.1:8000` to see the application running. Thanks to `FastAPI` versatility, you can also check out an auto-generated Swagger API documentation at `http://127.0.0.1:8000/docs`.

## Deploy Instructions
The application uses Docker for establishing an isolated server environment. There are plans to develop a CI/CD pipeline to leverage both developent and deployment in the future. Therefore, for now, we intend to perform this process manually. Here are the steps:

- Clone the repository and navigate into the root folder.

    - **Important:** *Either* use a **provided** `.env` **file** *or* create **a new one** which will issue environment variables for the application to work. You can check the template at `.env.example`. Fill it in with all required information.

- Create the custom docker image And then run docker compose:

    `docker build -t thina-ai-api-test:0.1 .`

- And then run docker compose:

    `docker-compose up`

- You may also check how it's running:

    `docker-compose ps -a`

- If by any chance, you think it's necessary, you might as well stop the service:

    `docker-compose down`

By default, the application is set up to receive requests either at `http://localhost:8000/docs` or any provided URL provided by THINA's IT department, at port `8000`.

## Contribution guidelines

* Writing tests
* Code review
* Other guidelines
* (Under development...)

## Who do I talk to?
    
* THINA AI Team
    - *Repo Owner*: Amauri Holanda (email)
    - Gabriel (email)
    - Erik Jhones (email)