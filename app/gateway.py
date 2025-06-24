from fastapi import APIRouter
from app.routs.ride_routs import router as rides_router
from app.routs.view_stat_routs import router as view_router
from app.routs.login_routs import router as login_router
from app.routs.governance_routs import router as governanca_router
from app.routs.client_routs import router as client_router
from app.routs.car_routs import router as car_router
from app.routs.company_routs import router as company_router
from app.routs.hotel_routs import router as hotel_router

router = APIRouter()

router.include_router(rides_router, prefix="/consulting", tags=["rides_router"])
router.include_router(view_router, prefix="/view", tags=["view_router"])
router.include_router(login_router, prefix="/login", tags=["login_router"])
router.include_router(governanca_router, prefix="/governanca", tags=["governanca_router"])
router.include_router(client_router, prefix="/client", tags=["client_router"])
router.include_router(car_router, prefix="/car", tags=["car_router"])
router.include_router(company_router, prefix="/company", tags=["company_router"])
router.include_router(hotel_router, prefix="/hotel", tags=["hotel_router"]) 