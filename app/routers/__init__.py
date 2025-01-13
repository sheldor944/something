from fastapi import APIRouter
from routers import token, auth, img, profile, event, hall_of_fame, stock

router = APIRouter(
    prefix="/api/v1"
)

router.include_router(token.router)
router.include_router(auth.router)
router.include_router(img.router)
router.include_router(profile.router)
router.include_router(event.router)
router.include_router(hall_of_fame.router)
router.include_router(stock.router)



