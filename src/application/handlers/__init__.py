from aiogram.dispatcher.router import Router

from .get_fio import router as fio_router
from .get_phone import router as phone_router
from .personal_data import router as pd_router
from .get_region import router as region_router
from .get_email import router as email_router
from .start import router as start_router, start_command_router

router = Router(name=__name__)

router.include_router(start_command_router)
router.include_router(pd_router)
router.include_router(fio_router)
router.include_router(phone_router)
router.include_router(email_router)
router.include_router(region_router)
router.include_router(start_router)
