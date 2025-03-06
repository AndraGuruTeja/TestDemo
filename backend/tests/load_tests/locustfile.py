from locust import HttpUser, task, between
import random

# List of cities to simulate requests for
CITIES = ["london", "paris", "berlin", "tokyo", "newyork"]

class WeatherUser(HttpUser):
    """
    Locust user class to simulate API requests for weather data.
    """
    wait_time = between(1, 3)  # Simulate users waiting between 1 and 3 seconds

    def on_start(self):
        """
        Called when a user starts. Authenticate and get a token.
        """
        # Authenticate and get a token
        response = self.client.post("/token", data={
            "username": "test@example.com",
            "password": "testpass"
        })
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @task(5)  # Higher weight: this task will be executed more frequently
    def get_current_weather(self):
        """
        Simulate fetching current weather for a random city.
        """
        city = random.choice(CITIES)
        self.client.get(f"/weather/{city}", headers=self.headers)

    @task(3)  # Medium weight
    def get_historical_data(self):
        """
        Simulate fetching historical weather data for a random city.
        """
        city = random.choice(CITIES)
        self.client.get(
            f"/weather/history/{city}",
            params={"days": random.randint(1, 10)},
            headers=self.headers
        )

    @task(2)  # Lower weight
    def get_weather_trends(self):
        """
        Simulate fetching weather trends for a random city.
        """
        city = random.choice(CITIES)
        self.client.get(
            f"/weather/trends/{city}",
            params={"days": random.randint(1, 10)},
            headers=self.headers
        )