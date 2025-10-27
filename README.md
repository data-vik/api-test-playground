# API Test Playground


Spin up a small FastAPI app with CRUD endpoints to practice API testing, contract testing, negative testing, property-based testing, Postman/Newman runs, and simple performance testing.


## Quick start
```bash
# 1) Clone and enter
# git clone <this-repo>
cd api-test-playground


# 2) Start the API
make run
# or with Docker
docker compose up --build api


# 3) Open docs
open http://localhost:8000/docs


# 4) Run tests
make test


# 5) Fuzz against OpenAPI
make fuzz


# 6) Postman -> Newman
make postman


# 7) Locust UI
make perf # then open http://localhost:8089
