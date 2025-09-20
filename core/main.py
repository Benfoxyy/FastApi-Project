from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from tasks.routes import router as tasks_router
from users.routes import router as users_router

app = FastAPI(
    title="Todo Application",
    description=(
        "A simple and efficient Todo management API built with FastAPI. "
        "This API allows users to create, retrieve, update, and delete tasks. "
        "It is designed for task tracking and productivity improvement."
    ),
    version="1.0.0",
    terms_of_service="https://example.com/terms/",
    contact={
        "name": "Ali Bigdeli",
        "url": "https://thealibigdeli.ir",
        "email": "benxfoxy@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(tasks_router)
app.include_router(users_router)
