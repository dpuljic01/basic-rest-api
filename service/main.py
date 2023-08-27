from fastapi import FastAPI

from service.api.fact.endpoint import fact_router
from service.api.popular.endpoint import popular_router
from service.database.db import init_db

app = FastAPI()

app.include_router(fact_router)
app.include_router(popular_router)

app.on_event("startup")(init_db)
