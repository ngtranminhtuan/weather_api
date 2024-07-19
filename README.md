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
source env/bin/activate
pip install --upgrade pip wheel setuptools
pip install -r requirements.txt
uvicorn main:app --reload

# Access for test apis
http://127.0.0.1:8000/docs

# Open other terminal to run locust for monitor service
locust -f locustfile.py
```

```
logs
(env) ➜  weather_api git:(main) ✗ uvicorn main:app --reload

INFO:     Will watch for changes in these directories: ['/Users/tuan/Downloads/weather_api']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [93089] using WatchFiles
INFO:     Started server process [93108]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:51359 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:51359 - "GET /openapi.json HTTP/1.1" 200 OK
INFO:     127.0.0.1:51364 - "GET /api/v1/weather?location=Osaka HTTP/1.1" 200 OK
INFO:     127.0.0.1:51375 - "POST /api/v1/chat_weather HTTP/1.1" 200 OK
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

====================================================

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
(env) ➜  weather_api git:(main) ✗ pytest
=================================================== test session starts ===================================================
platform darwin -- Python 3.10.14, pytest-8.2.2, pluggy-1.5.0
rootdir: /Users/tuan/Downloads/weather_api
plugins: asyncio-0.23.7, anyio-4.4.0
asyncio: mode=strict
collected 6 items

tests/test_llm_factory.py ..                                                                                        [ 33%]
tests/test_openai_service.py ..                                                                                     [ 66%]
tests/test_weather_service.py ..                                                                                    [100%]

==================================================== 6 passed in 0.24s ====================================================
```
