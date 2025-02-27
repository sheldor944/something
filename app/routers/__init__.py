from fastapi import APIRouter
from routers import token, auth, img, profile, stock, trade, prediction, account

router = APIRouter(
    prefix="/api/v1"
)

router.include_router(token.router)
router.include_router(auth.router)
router.include_router(img.router)
router.include_router(profile.router)

router.include_router(stock.router)
router.include_router(trade.router)
router.include_router(prediction.router)
router.include_router(account.router)



