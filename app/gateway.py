from fastapi import APIRouter
from routs.ride_routs import router as rides_router
from routs.view_stat_routs import router as view_router
from routs.login_routs import router as login_router
from routs.governance_routs import router as governanca_router
from routs.client_routs import router as client_router
from routs.car_routs import router as car_router
from routs.company_routs import router as company_router
from routs.hotel_routs import router as hotel_router
# from routs.health_routs import router as health_router

router = APIRouter()

# APIs de Sistema/Monitoramento
# router.include_router(health_router, prefix="/system", tags=["System"])

# APIs de Autenticação
router.include_router(login_router, prefix="/auth", tags=["Authentication"])

# APIs de Negócio - Usuários
router.include_router(client_router, prefix="/api/v1/clients", tags=["Clients"])

# APIs de Negócio - Transporte
router.include_router(rides_router, prefix="/api/v1/rides", tags=["Rides"])
router.include_router(car_router, prefix="/api/v1/cars", tags=["Cars"])

# APIs de Negócio - Parceiros
router.include_router(company_router, prefix="/api/v1/companies", tags=["Companies"])
router.include_router(hotel_router, prefix="/api/v1/hotels", tags=["Hotels"])

# APIs de Gestão
router.include_router(governanca_router, prefix="/api/v1/governance", tags=["Governance"])
router.include_router(view_router, prefix="/api/v1/analytics", tags=["Analytics"])