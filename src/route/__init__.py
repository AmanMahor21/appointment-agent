from .telegram import router as telegram_router


def register_routes(app):
    app.include_router(telegram_router)
