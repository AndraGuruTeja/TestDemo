# from locust import HttpUser, task, between
# import json
# import random

# class WeatherUser(HttpUser):
#     wait_time = between(1, 3)  # Simulate realistic user behavior
#     token = None  # Store authentication token
#     headers = {}  # Store headers

#     def on_start(self):
#         """Runs when a Locust user starts."""
#         self.authenticate()

#     def authenticate(self):
#         """Get authentication token."""
#         response = self.client.post("/token", data={"username": "user", "password": "password"})
#         if response.status_code == 200:
#             self.token = response.json().get("access_token")
#             self.headers = {"Authorization": f"Bearer {self.token}"}
#         else:
#             print(f"[ERROR] Authentication failed: {response.status_code}, {response.text}")

#     @task(1)
#     def get_weather(self):
#         """Fetch current weather for a random city."""
#         city = random.choice(["Bangalore", "New York", "London", "Tokyo", "Sydney"])
#         response = self.client.get(f"/weather/{city}", headers=self.headers)
#         if response.status_code != 200:
#             print(f"[ERROR] Failed GET /weather/{city}: {response.status_code}, {response.text}")

#     @task(2)
#     def get_historical_data(self):
#         """Fetch historical weather data for a random city."""
#         city = random.choice(["Bangalore", "New York", "London", "Tokyo", "Sydney"])
#         response = self.client.get(f"/weather/history/{city}?days=7", headers=self.headers)
#         if response.status_code != 200:
#             print(f"[ERROR] Failed GET /weather/history/{city}: {response.status_code}, {response.text}")

#     @task(2)
#     def get_weather_trends(self):
#         """Fetch weather trends for a random city."""
#         city = random.choice(["Bangalore", "New York", "London", "Tokyo", "Sydney"])
#         response = self.client.get(f"/weather/trends/{city}?days=7", headers=self.headers)
#         if response.status_code != 200:
#             print(f"[ERROR] Failed GET /weather/trends/{city}: {response.status_code}, {response.text}")
