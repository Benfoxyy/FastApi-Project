from fastapi import FastAPI
from contextlib import asynccontextmanager
from tasks.routes import router as tasks_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("FastAPI is starting")

    yield

    print("FastAPI is down")

app = FastAPI(
    lifespan=lifespan,
    title="Todo App Api",
    description="This is a complete ToDo list with tons of useful features",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Benyamin Medghalchi",
        "url": "https://benfoxyy.github.io/Resume/",
        "email": "benxfoxy@gmail.com",
    },
    license_info={"name": "MIT"},
    docs_url="/swagger",
    )

app.include_router(tasks_router, prefix='/todo')