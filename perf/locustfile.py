from locust import HttpUser, task, between

class ApiUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def list_health(self):
        self.client.get("/health")

    @task
    def create_user_and_item(self):
        u = self.client.post("/users", json={"email": "load@example.com", "full_name": "Load"})
        if u.status_code == 201:
            uid = u.json()["id"]
            self.client.post("/items", json={"name": "LoadItem", "price": 1.23, "owner_id": uid})