from fastapi import FastAPI

from app.Controllers.TicketsController import router as tickets_router
from app.Controllers.EventsController import router as events_router
from app.Controllers.PacketsController import router as packets_router

app = FastAPI(title="Event WebService")

app.include_router(events_router)
app.include_router(packets_router)
app.include_router(tickets_router)

@app.get("/")
def root():
    return {"status": "OK", "docs": "/docs"}
