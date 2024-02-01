from aiogram import Router
from .geo_stats import geo_router
from .buyer_stats import buyer_router
from .project_stats import project_router

stat_filter_router = Router()

stat_filter_router.include_routers(geo_router, buyer_router, project_router)
