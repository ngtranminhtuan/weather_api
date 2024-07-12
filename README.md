# Weather API

This project is a weather API service built with FastAPI and uses Locust for load testing. The project is containerized using Docker and Docker Compose.

## Table of Contents

- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running the Project](#running-the-project)
- [Running Locust](#running-locust)
- [Endpoints](#endpoints)
- [Pytest](#pytest)

## Project Structure
```
.
├── app
│   ├── api
│   │   ├── __init__.py
│   │   └── v1
│   │       └── weather.py # API endpoints for weather-related operations
│   ├── config
│   │   ├── __init__.py
│   │   └── settings.py # Configuration settings for the application
│   ├── models
│   │   ├── __init__.py
│   │   └── weather.py # Pydantic models for data validation and serialization
│   ├── services
│       ├── __init__.py
│       ├── llm_factory.py # Factory for creating instances of language model services
│       ├── openai_service.py # Service for interacting with OpenAI API
│       └── weather_service.py # Business logic for weather-related operations
│   
├── tests # Unit tests for the application
│   ├── __init__.py
│   ├── test_openai_tool.py # Unit tests for OpenAI utility functions
│   └── test_weather_service.py # Unit tests for weather-related services
├── locustfile.py # Load testing script for Locust
├── main.py # Entry point for the FastAPI application
├── requirements.txt # Python dependencies for the project
├── Dockerfile # Dockerfile for building the Docker image
├── docker-compose.yml # Docker Compose file for setting up the multi-container environment
└── README.md # Documentation and setup instructions for the project

```

## Prerequisites

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/ngtranminhtuan/weather_api.git
    cd weather_api
    ```

2. Build and start the Docker containers:

    ```bash
    docker-compose up --build
    ```

3. We can run without Docker using vitual environment:
```
python3.10 -m venv env
pip install --upgrade pip wheel setuptools
pip install -r requirements.txt
uvicorn main:app --reload

# Access for test apis
http://127.0.0.1:8000/docs

# Open other terminal to run locust for monitor service
locust -f locustfile.py
```

## Running the Project

After running `docker-compose up --build`, the FastAPI server should be up and running. You can access it at:

```
http://localhost:8000
```


### Running Locust

To run Locust for load testing, ensure the Docker containers are up and running. Then, you can access the Locust web interface at:

```
http://localhost:8089
```
![image alt text](<images/locust.png>)
![image alt text](<images/system.jpeg>)

## Endpoints

![image alt text](<images/read_weather.png>)
### Get Current Weather

- **Endpoint:** `/api/v1/weather`
- **Method:** `GET`
- **Query Parameters:**
  - `location` (string): The city and country (e.g., `Osaka,jp`)

![image alt text](<images/chat_weather.png>)
### Chat Weather

- **Endpoint:** `/api/v1/chat_weather`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "messages": [
      {"role": "user", "content": "What's the weather in Tokyo?"}
    ]
  }

## Pytest
```
(env) ➜  weather_api git:(218ac96) pytest 
===================================================================================== test session starts ======================================================================================
platform linux -- Python 3.10.12, pytest-8.2.2, pluggy-1.5.0
rootdir: /home/tuan/Downloads/weather_api
plugins: anyio-4.4.0, asyncio-0.23.7
asyncio: mode=strict
collected 7 items                                                                                                                                                                              

tests/test_llm_factory.py ..                                                                                                                                                             [ 28%]
tests/test_openai_service.py ..                                                                                                                                                          [ 57%]
tests/test_weather_service.py ...                                                                                                                                                        [100%]

====================================================================================== 7 passed in 0.66s =======================================================================================
```