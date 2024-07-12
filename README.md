
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
