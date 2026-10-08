# backend/app/api/v1/requests.py
from fastapi import APIRouter
from . import requests_main, requests_search
from .dependencies import get_db

router = APIRouter(prefix="/requests", tags=["Requests"])

router.include_router(requests_main.router)
router.include_router(requests_search.router)

__all__ = ["router", "get_db"]