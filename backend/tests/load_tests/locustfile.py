
# # backend/tests/load_tests/locustfile.py
# from locust import HttpUser, task, between
# import random
# import uuid

# class WeatherUser(HttpUser):
#     wait_time = between(1, 3)
    
#     def on_start(self):
#         # Create unique credentials for each virtual user
#         self.username = f"loadtest_{uuid.uuid4()}@example.com"
#         self.password = "loadtest_pass123"
        
#         # Register user first
#         self.client.post("/register", json={
#             "email": self.username,
#             "password": self.password
#         })
        
#         # Login to get token
#         response = self.client.post("/token", data={
#             "username": self.username,
#             "password": self.password
#         })
        
#         if response.status_code == 200:
#             self.token = response.json()["access_token"]
#             self.headers = {"Authorization": f"Bearer {self.token}"}
#         else:
#             self.token = None
#             self.headers = {}

#     @task(5)
#     def get_weather(self):
#         if self.token:
#             cities = ["London", "New York", "Tokyo", "Paris", "Berlin"]
#             self.client.get(
#                 f"/weather/{random.choice(cities)}",
#                 headers=self.headers
#             )

#     @task(2)
#     def get_history(self):
#         if self.token:
#             cities = ["London", "New York", "Tokyo"]
#             self.client.get(
#                 f"/weather/history/{random.choice(cities)}?days=7",
#                 headers=self.headers
#             )

#     @task(1)
#     def get_trends(self):
#         if self.token:
#             cities = ["London", "New York"]
#             self.client.get(
#                 f"/weather/trends/{random.choice(cities)}?days=7",
#                 headers=self.headers
#             )








from locust import HttpUser, task, between, events
import random
import uuid

# Global counter to track total executions
execution_count = 0
MAX_EXECUTIONS = 100  # Set the maximum number of executions before stopping

class WeatherUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # Create unique credentials for each virtual user
        self.username = f"loadtest_{uuid.uuid4()}@example.com"
        self.password = "loadtest_pass123"
        
        # Register user first
        self.client.post("/register", json={
            "email": self.username,
            "password": self.password
        })
        
        # Login to get token
        response = self.client.post("/token", data={
            "username": self.username,
            "password": self.password
        })
        
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            self.token = None
            self.headers = {}

    @task(5)
    def get_weather(self):
        global execution_count
        if self.token and execution_count < MAX_EXECUTIONS:
            cities = ["London", "New York", "Tokyo", "Paris", "Berlin"]
            self.client.get(
                f"/weather/{random.choice(cities)}",
                headers=self.headers
            )
            execution_count += 1
            self.check_execution_limit()

    @task(2)
    def get_history(self):
        global execution_count
        if self.token and execution_count < MAX_EXECUTIONS:
            cities = ["London", "New York", "Tokyo"]
            self.client.get(
                f"/weather/history/{random.choice(cities)}?days=7",
                headers=self.headers
            )
            execution_count += 1
            self.check_execution_limit()

    @task(1)
    def get_trends(self):
        global execution_count
        if self.token and execution_count < MAX_EXECUTIONS:
            cities = ["London", "New York"]
            self.client.get(
                f"/weather/trends/{random.choice(cities)}?days=7",
                headers=self.headers
            )
            execution_count += 1
            self.check_execution_limit()

    def check_execution_limit(self):
        """Stop the test if the maximum number of executions is reached."""
        if execution_count >= MAX_EXECUTIONS:
            print(f"Stopping test: Reached maximum executions ({MAX_EXECUTIONS})")
            self.environment.runner.quit()

