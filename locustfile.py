from locust import HttpUser, task, between

class WeatherApiUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def get_weather(self):
        self.client.get("/api/v1/weather?location=Osaka,jp")

    @task
    def post_chat_weather(self):
        data = {
            "messages": [
                {"role": "user", "content": "What's the weather in Osaka?"}
            ]
        }
        self.client.post("/api/v1/chat_weather", json=data)
