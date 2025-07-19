from fastapi.routing import APIRouter

hubspot_router = APIRouter(
    prefix="/hubspot", tags=["hubspot"]
)

from . import views