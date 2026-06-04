import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, FSInputFile
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8692931256:AAEIIC1zo-iqGgTwDNb0D4uTGKt9CqyYdes")
WEBAPP_URL = os.environ.get("WEBAPP_URL", "https://nebula-app-3.onrender.com")
IMAGE_PATH = "static/welcome.jpg"

WELCOME_TEXT = """Вас приветствует <b>ORION parcer</b> 🚗

Это приложение создано для вас, и для повышения комфорта вашей работы 💻

Приложение абсолютно бесплатное для пользователей которые состоят в команде <b>ORION 7+ дней</b> ⏱

Для остальных есть прайсы на использование 📥
➖ доступ на 24 часа — <b>5$</b>
➖ доступ на 48 часов — <b>9$</b>
➖ доступ на три дня — <b>25$</b>
➖ доступ на две недели — <b>100$</b>
➖ доступ на месяц — <b>300$</b>

Для покупки а также более детальной информации пишите — @dmitryn1

Чтобы вступить в команду ORION пишите этому человеку — @pexaab"""

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


def get_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Перейти на наш сайт", web_app=WebAppInfo(url=WEBAPP_URL))],
        [
            InlineKeyboardButton(text="💎 Купить доступ", url="https://t.me/dmitryn1"),
            InlineKeyboardButton(text="👥 Вступить в ORION", url="https://t.me/pexaab"),
        ],
    ])


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    try:
        if os.path.exists(IMAGE_PATH):
            photo = FSInputFile(IMAGE_PATH)
            await message.answer_photo(photo=photo, caption=WELCOME_TEXT, reply_markup=get_kb())
        else:
            await message.answer(text=WELCOME_TEXT, reply_markup=get_kb())
        logger.info(f"User {message.from_user.id} (@{message.from_user.username}) - /start")
    except Exception as e:
        logger.error(f"Error /start: {e}")
        await message.answer(text=WELCOME_TEXT, reply_markup=get_kb())


@dp.message(Command("app"))
async def cmd_app(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🚀 Открыть ORION parcer", web_app=WebAppInfo(url=WEBAPP_URL))
    ]])
    await message.answer("Нажмите кнопку чтобы открыть приложение 👇", reply_markup=kb)


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "📋 <b>Команды:</b>\n\n/start — главное меню\n/app — открыть приложение\n/help — помощь",
        reply_markup=get_kb()
    )


async def run_bot():
    logger.info("🤖 ORION bot starting...")
    logger.info(f"📱 WebApp: {WEBAPP_URL}")
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands([
        types.BotCommand(command="start", description="🚀 Главное меню"),
        types.BotCommand(command="app", description="📱 Открыть приложение"),
        types.BotCommand(command="help", description="❓ Помощь"),
    ])
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(run_bot())
