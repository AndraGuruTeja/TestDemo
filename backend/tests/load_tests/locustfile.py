
# from locust import HttpUser, task, between, events
# import random
# import uuid
# import threading

# MAX_EXECUTIONS = 100  # Total allowed requests
# execution_lock = threading.Lock()  # Prevent race conditions
# execution_count = 0  # Track total executions across all users

# class WeatherUser(HttpUser):
#     wait_time = between(1, 3)

#     def on_start(self):
#         """Register and log in the user on start."""
#         self.username = f"loadtest_{uuid.uuid4()}@example.com"
#         self.password = "loadtest_pass123"

#         # Register the user
#         self.client.post("/register", json={
#             "email": self.username,
#             "password": self.password
#         })

#         # Login to get the token
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
#         """Fetch weather for a random city."""
#         self.execute_request(f"/weather/{random.choice(['London', 'New York', 'Tokyo', 'Paris', 'Berlin'])}")

#     @task(2)
#     def get_history(self):
#         """Fetch weather history."""
#         self.execute_request(f"/weather/history/{random.choice(['London', 'New York'])}?days=7")

#     @task(1)
#     def get_trends(self):
#         """Fetch weather trends."""
#         self.execute_request(f"/weather/trends/{random.choice(['London', 'New York'])}?days=7")

#     def execute_request(self, endpoint):
#         """Helper function to execute requests while tracking the global execution count."""
#         global execution_count
#         with execution_lock:  # Prevents race conditions
#             if execution_count >= MAX_EXECUTIONS:
#                 return  # Stop executing further tasks
            
#             execution_count += 1

#         self.client.get(endpoint, headers=self.headers)

#         # If max executions are reached, stop the test
#         with execution_lock:
#             if execution_count >= MAX_EXECUTIONS:
#                 print(f"Stopping test: Reached max executions ({MAX_EXECUTIONS})")
#                 self.environment.runner.quit()

# # Ensure graceful shutdown when max executions are reached
# @events.quitting.add_listener
# def on_quit(environment, **kwargs):
#     print("Test completed successfully!")




from locust import HttpUser, task, between, events
import random
import uuid
import threading

MAX_EXECUTIONS = 100  # Total allowed requests
execution_lock = threading.Lock()  # Prevent race conditions
execution_count = 0  # Track total executions across all users


class WeatherUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Register and log in the user on start."""
        self.username = f"loadtest_{uuid.uuid4()}@example.com"
        self.password = "loadtest_pass123"

        try:
            # Register the user
            register_response = self.client.post("/register", json={
                "email": self.username,
                "password": self.password
            })

            if register_response.status_code not in [200, 201]:
                print(f"Failed to register: {register_response.text}")
                return

            # Login to get the token
            token_response = self.client.post("/token", data={
                "username": self.username,
                "password": self.password
            })

            if token_response.status_code == 200:
                self.token = token_response.json().get("access_token", "")
                self.headers = {"Authorization": f"Bearer {self.token}"}
            else:
                print(f"Failed to authenticate: {token_response.text}")
                self.token = None
                self.headers = {}

        except Exception as e:
            print(f"Error during setup: {e}")

    @task(5)
    def get_weather(self):
        """Fetch weather for a random city."""
        self.execute_request(f"/weather/{random.choice(['London', 'New York', 'Tokyo', 'Paris', 'Berlin'])}")

    @task(2)
    def get_history(self):
        """Fetch weather history."""
        self.execute_request(f"/weather/history/{random.choice(['London', 'New York'])}?days=7")

    @task(1)
    def get_trends(self):
        """Fetch weather trends."""
        self.execute_request(f"/weather/trends/{random.choice(['London', 'New York'])}?days=7")

    def execute_request(self, endpoint):
        """Helper function to execute requests while tracking the global execution count."""
        global execution_count

        with execution_lock:  # Prevents race conditions
            if execution_count >= MAX_EXECUTIONS:
                return  # Stop executing further tasks

            execution_count += 1

        try:
            response = self.client.get(endpoint, headers=self.headers)

            if response.status_code != 200:
                print(f"Request failed: {endpoint} -> {response.status_code} {response.text}")

        except Exception as e:
            print(f"Error making request to {endpoint}: {e}")

        # If max executions are reached, stop the test
        with execution_lock:
            if execution_count >= MAX_EXECUTIONS:
                print(f"Stopping test: Reached max executions ({MAX_EXECUTIONS})")
                self.environment.runner.quit()


# Ensure graceful shutdown when max executions are reached
@events.quitting.add_listener
def on_quit(environment, **kwargs):
    print("Test completed successfully!")





