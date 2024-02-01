import asyncio
from aiogram import Bot, Dispatcher
from handlers.basic import basic_router
from handlers.stats import stat_filter_router
from handlers.add_filter import add_filters_router
from handlers.delete_filter import delete_filter_router
from middlewares.db_middleware import DataBaseMiddelware
from sql.db import create_pool
from config import settings

session_factory = create_pool(dsn="sqlite+aiosqlite:///filters.db",
                              enable_logging=True)


async def main():
    bot = Bot(token=settings.token)
    dp = Dispatcher()
    dp.update.outer_middleware(DataBaseMiddelware(session_factory))
    dp.include_router(basic_router)
    dp.include_router(stat_filter_router)
    dp.include_router(add_filters_router)
    dp.include_router(delete_filter_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
