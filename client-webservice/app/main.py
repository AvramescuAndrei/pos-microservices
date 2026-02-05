from fastapi import FastAPI
from Controllers.ClientsController import router as clients_router

app = FastAPI(title="Client WebService")

app.include_router(clients_router)


@app.get("/")
def root():
    return {"status": "ok", "service": "client-webservice", "docs": "/docs"}
