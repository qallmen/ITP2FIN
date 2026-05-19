import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import DatabaseManager
from utils import calculate_nearest_places, format_feedback

LOCALIZATION = {
    "en": {
        "welcome": "🏙 Welcome to the Professional Astana Guide Bot!",
        "nearest": "📍 Nearest Cool Places",
        "restaurants": "🍴 Restaurants",
        "parks": "🌳 Parks",
        "libraries": "📚 Libraries",
        "developers": "👨‍💻 Developers",
        "help": "🆘 Need Help?",
        "top_nearest": "📍 **Top Coolest Places Nearest to You:**\n\n",
        "no_db": "No elements loaded inside database configuration.",
        "open_2gis": "🗺 Open in 2GIS",
        "leave_feedback": "✍️ Leave Feedback",
        "next": "➡️ Another one (Next)",
        "rating": "Rating",
        "receipt": "Receipt/Entry",
        "description": "Description",
        "reviews": "User Reviews",
        "type_feedback": "✍️ Please type your review text for",
        "saved_feedback": "✅ Your review was saved permanently!",
        "dev_team": "🚀 **Step by Step Development Team:**\n• @qallmen\n• @arabek127\n• @bzglnazerke\n\nClick the button below to submit directly an instant message to all working developers.",
        "give_dev_fb": "📣 Give Developers Feedback",
        "type_dev_fb": "📥 Type your message for the development team. It will be routed immediately:",
        "dev_fb_sent": "🚀 Thank you! Your feedback message has been transmitted directly.",
        "help_title": "🚨 **Emergency Help Support**",
        "help_desc": "Please describe your problem or question in one message. It will be sent immediately to all our developers as an urgent ticket!",
        "help_sent": "🚀 **Sent!** Our team has been notified. We will get back to you as soon as possible!",
        "no_feedback": "No feedback left yet. Be the first to add your experience!"
    },
    "kz": {
        "welcome": "🏙 Кәсіби Астана Жолсілтеуші Ботына қош келдіңіз!",
        "nearest": "📍 Жакын Маңдағы Керемет Жерлер",
        "restaurants": "🍴 Мейрамханалар",
        "parks": "🌳 Саябақтар",
        "libraries": "📚 Кітапханалар",
        "developers": "👨‍💻 Әзірлеушілер",
        "help": "🆘 Көмек Қажет пе?",
        "top_nearest": "📍 **Сізге ең жақын орналасқан үздік жерлер:**\n\n",
        "no_db": "Дерекқорда ештеңе табылмады.",
        "open_2gis": "🗺 2GIS-те ашу",
        "leave_feedback": "✍️ Пікір қалдыру",
        "next": "➡️ Келесісі",
        "rating": "Рейтинг",
        "receipt": "Орташа чек/Кіру",
        "description": "Сипаттамасы",
        "reviews": "Пайдаланушылардың пікірлері",
        "type_feedback": "✍️ Мына жерге өз пікіріңізді жазыңыз:",
        "saved_feedback": "✅ Сіздің пікіріңіз сәтті сақталды!",
        "dev_team": "🚀 **Step by Step Әзірлеушілер Командасы:**\n• @qallmen\n• @arabek127\n• @bzglnazerke\n\nӘзірлеушілерге тікелей хабарлама жіберу үшін төмендегі батырманы басыңыз.",
        "give_dev_fb": "📣 Әзірлеушілерге пікір қалдыру",
        "type_dev_fb": "📥 Әзірлеушілер командасына өз хабарламаңызды жазыңыз. Ол бірден жеткізіледі:",
        "dev_fb_sent": "🚀 Рақмет! Сіздің хабарламаңыз әзірлеушілерге сәтті жіберілді.",
        "help_title": "🚨 **Шұғыл Көмек Көрсету**",
        "help_desc": "Мәселеңізді немесе сұрағыңызды бір хабарламамен сипаттаңыз. Ол барлық әзірлеушілерге шұғыл билет ретінде жіберіледі!",
        "help_sent": "🚀 **Жіберілді!** Біздің командаға хабарландыру түсті. Жақын арада жауап береміз!",
        "no_feedback": "Пікірлер әлі қалдырылмаған. Бірінші болып өз әсеріңізбен бөлісіңіз!"
    },
    "ru": {
        "welcome": "🏙 Добро пожаловать в профессиональный бот-гид по Астане!",
        "nearest": "📍 Ближайшие крутые места",
        "restaurants": "🍴 Рестораны",
        "parks": "🌳 Парки",
        "libraries": "📚 Библиотеки",
        "developers": "👨‍💻 Разработчики",
        "help": "🆘 Нужна помощь?",
        "top_nearest": "📍 **Топ ближайших к вам крутых мест:**\n\n",
        "no_db": "Данные в базе данных конфигурации не найдены.",
        "open_2gis": "🗺 Открыть в 2GIS",
        "leave_feedback": "✍️ Оставить отзыв",
        "next": "➡️ Следующее",
        "rating": "Rating",
        "receipt": "Средний чек/Вход",
        "description": "Описание",
        "reviews": "Отзывы пользователей",
        "type_feedback": "✍️ Пожалуйста, напишите ваш отзыв для",
        "saved_feedback": "✅ Ваш отзыв успешно сохранен в базе данных!",
        "dev_team": "🚀 **Команда разработчиков Step by Step:**\n• @qallmen\n• @arabek127\n• @bzglnazerke\n\nНажмите кнопку ниже, чтобы отправить мгновенное сообщение всем разработчикам.",
        "give_dev_fb": "📣 Оставить отзыв разработчикам",
        "type_dev_fb": "📥 Напишите ваше сообщение для команды разработчиков. Оно будет доставлено немедленно:",
        "dev_fb_sent": "🚀 Спасибо! Ваше сообщение было передано напрямую команде.",
        "help_title": "🚨 **Экстренная Служба Поддержки**",
        "help_desc": "Пожалуйста, опишите вашу проблему или вопрос в одном сообщении. Оно будет немедленно отправлено всем разработчикам!",
        "help_sent": "🚀 **Отправлено!** Наша команда уведомлена. Мы свяжемся с вами как можно скорее!",
        "no_feedback": "Отзывов пока нет. Будьте первым, кто поделится своим опытом!"
    }
}

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("CRITICAL ERROR: BOT_TOKEN variable not configured inside .env storage environment configuration file.")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
db = DatabaseManager()

DEVELOPER_IDS = [7287838167, 802237634, 1049071247]


class BotStates(StatesGroup):
    waiting_for_language = State()
    waiting_for_feedback = State()
    waiting_for_dev_feedback = State()
    waiting_for_help = State()


def get_language_kb():
    return types.ReplyKeyboardMarkup(keyboard=[
        [types.KeyboardButton(text="🇬🇧 English"), types.KeyboardButton(text="🇰🇿 Қазақша"), types.KeyboardButton(text="🇷🇺 Русский")]
    ], resize_keyboard=True)


def get_main_kb(lang):
    texts = LOCALIZATION[lang]
    return types.ReplyKeyboardMarkup(keyboard=[
        [types.KeyboardButton(text=texts["nearest"], request_location=True)],
        [types.KeyboardButton(text=texts["restaurants"]), types.KeyboardButton(text=texts["parks"])],
        [types.KeyboardButton(text=texts["libraries"]), types.KeyboardButton(text=texts["developers"])],
        [types.KeyboardButton(text=texts["help"])]
    ], resize_keyboard=True)


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("🌐 Choose your language / Тілді таңдаңыз / Выберите язык:", reply_markup=get_language_kb())
    await state.set_state(BotStates.waiting_for_language)


@dp.message(BotStates.waiting_for_language)
async def process_language_choice(message: types.Message, state: FSMContext):
    if message.text == "🇬🇧 English":
        lang = "en"
    elif message.text == "🇰🇿 Қазақша":
        lang = "kz"
    elif message.text == "🇷🇺 Русский":
        lang = "ru"
    else:
        await message.answer("Please use the keyboard buttons to pick a language.")
        return

    await state.update_data(user_lang=lang)
    texts = LOCALIZATION[lang]
    await message.answer(texts["welcome"], reply_markup=get_main_kb(lang))
    await state.set_state(None)


@dp.message(F.location)
async def handle_location(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get("user_lang", "en")
    texts = LOCALIZATION[lang]

    all_items = db.get_all_places()
    if not all_items:
        await message.answer(texts["no_db"])
        return

    nearest = calculate_nearest_places(message.location.latitude, message.location.longitude, all_items, limit=10)

    response = texts["top_nearest"]
    for i, p in enumerate(nearest, 1):
        desc = p.get(f'description_{lang}', p['description_en'])
        response += f"{i}. **{p['name']}** ({p['distance']:.2f} km)\n_{desc}_\n\n"
    await message.answer(response, parse_mode="Markdown")
    await message.answer_location(latitude=nearest[0]['lat'], longitude=nearest[0]['lon'])


async def send_place_card(message_or_call, category, index, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get("user_lang", "en")
    texts = LOCALIZATION[lang]

    places = db.get_places_by_category(category)
    if not places:
        target = message_or_call.message if isinstance(message_or_call, types.CallbackQuery) else message_or_call
        await target.answer(texts["no_db"])
        return

    item = places[index % len(places)]
    reviews = db.get_reviews_by_place(item['name'])
    formatted_reviews = format_feedback(reviews, texts["no_feedback"])

    description = item.get(f'description_{lang}', item['description_en'])

    text = (
        f"🏆 **{item['name']}**\n"
        f"⭐ {texts['rating']}: `{item['rating']}` | 💰 {texts['receipt']}: `{item['average_receipt']}`\n\n"
        f"📝 *{texts['description']}*:\n{description}\n\n"
        f"💬 *{texts['reviews']}*:\n{formatted_reviews}"
    )

    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=texts["open_2gis"], url=item['link_2gis'])],
        [types.InlineKeyboardButton(text=texts["leave_feedback"], callback_data=f"write_{category}_{index}")],
        [types.InlineKeyboardButton(text=texts["next"], callback_data=f"next_{category}_{index}")]
    ])

    if isinstance(message_or_call, types.CallbackQuery):
        try:
            await message_or_call.message.edit_media(
                media=types.InputMediaPhoto(media=item['photo_url'], caption=text, parse_mode="Markdown"),
                reply_markup=kb
            )
        except Exception:
            try:
                await message_or_call.message.answer_photo(photo=item['photo_url'], caption=text, reply_markup=kb, parse_mode="Markdown")
                await message_or_call.message.delete()
            except Exception:
                await message_or_call.message.answer(text, reply_markup=kb, parse_mode="Markdown")
    else:
        try:
            await message_or_call.answer_photo(photo=item['photo_url'], caption=text, reply_markup=kb, parse_mode="Markdown")
        except Exception:
            await message_or_call.answer(text, reply_markup=kb, parse_mode="Markdown")

@dp.message(lambda msg: msg.text in [LOCALIZATION["en"]["restaurants"], LOCALIZATION["kz"]["restaurants"], LOCALIZATION["ru"]["restaurants"]])
async def show_restaurants(message: types.Message, state: FSMContext):
    await send_place_card(message, "rest", 0, state)


@dp.message(lambda msg: msg.text in [LOCALIZATION["en"]["parks"], LOCALIZATION["kz"]["parks"], LOCALIZATION["ru"]["parks"]])
async def show_parks(message: types.Message, state: FSMContext):
    await send_place_card(message, "park", 0, state)


@dp.message(lambda msg: msg.text in [LOCALIZATION["en"]["libraries"], LOCALIZATION["kz"]["libraries"], LOCALIZATION["ru"]["libraries"]])
async def show_libraries(message: types.Message, state: FSMContext):
    await send_place_card(message, "lib", 0, state)


@dp.callback_query(F.data.startswith("next_"))
async def handle_next_carousel(call: types.CallbackQuery, state: FSMContext):
    _, category, current_idx = call.data.split("_")
    next_idx = int(current_idx) + 1
    await send_place_card(call, category, next_idx, state)
    await call.answer()


@dp.callback_query(F.data.startswith("write_"))
async def init_place_feedback(call: types.CallbackQuery, state: FSMContext):
    _, category, idx = call.data.split("_")
    places = db.get_places_by_category(category)
    item = places[int(idx) % len(places)]

    await state.update_data(place_name=item['name'], category=category, index=idx)
    await call.message.answer(f"✍️ Please type your review text for *{item['name']}*:", parse_mode="Markdown")
    await state.set_state(BotStates.waiting_for_feedback)
    await call.answer()


@dp.message(BotStates.waiting_for_feedback)
async def process_place_feedback(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    place_name = state_data['place_name']

    db.add_review(place_name, message.text)

    lang = state_data.get("user_lang", "en")
    texts = LOCALIZATION[lang]
    await message.answer(texts["saved_feedback"])

    await send_place_card(message, state_data['category'], int(state_data['index']), state)
    await state.set_state(None)


@dp.message(lambda msg: msg.text in [LOCALIZATION["en"]["developers"], LOCALIZATION["kz"]["developers"], LOCALIZATION["ru"]["developers"]])
async def show_developers_menu(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get("user_lang", "en")
    texts = LOCALIZATION[lang]

    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=texts["give_dev_fb"], callback_data="dev_feedback_init")]
    ])
    await message.answer(texts["dev_team"], reply_markup=kb, parse_mode="Markdown")


@dp.callback_query(F.data == "dev_feedback_init")
async def init_dev_feedback(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("📥 Type your message for the development team. It will be routed immediately:")
    await state.set_state(BotStates.waiting_for_dev_feedback)
    await call.answer()


@dp.message(BotStates.waiting_for_dev_feedback)
async def route_dev_feedback(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get("user_lang", "en")
    texts = LOCALIZATION[lang]

    sender = message.from_user.username or message.from_user.full_name
    dispatch_alert_text = (
        f"🔔 **New Incoming Developer Feedback!**\n"
        f"👤 From: @{sender} (`{message.from_user.id}`)\n"
        f"💬 Message: {message.text}"
    )

    for dev_id in DEVELOPER_IDS:
        try:
            await bot.send_message(chat_id=dev_id, text=dispatch_alert_text, parse_mode="Markdown")
        except Exception as e:
            print(f"[ERROR] Не удалось отправить сообщение на ID {dev_id}: {e}")

    await message.answer(texts["dev_fb_sent"])
    await state.set_state(None)


@dp.message(lambda msg: msg.text in [LOCALIZATION["en"]["help"], LOCALIZATION["kz"]["help"], LOCALIZATION["ru"]["help"]])
async def init_help_request(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get("user_lang", "en")
    texts = LOCALIZATION[lang]

    await message.answer(f"{texts['help_title']}\n\n{texts['help_desc']}", parse_mode="Markdown")
    await state.set_state(BotStates.waiting_for_help)


@dp.message(BotStates.waiting_for_help)
async def route_help_to_devs(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get("user_lang", "en")
    texts = LOCALIZATION[lang]

    sender = message.from_user.username or message.from_user.full_name
    emergency_alert_text = (
        f"🚨 🔥 **URGENT HELP REQUIRED!** 🔥 🚨\n\n"
        f"👤 **From User:** @{sender} (`{message.from_user.id}`)\n"
        f"✉️ **Problem Description:** {message.text}"
    )

    for dev_id in DEVELOPER_IDS:
        try:
            await bot.send_message(chat_id=dev_id, text=emergency_alert_text, parse_mode="Markdown")
        except Exception as e:
            print(f"[ERROR] Не удалось отправить сигнал о помощи на ID {dev_id}: {e}")

    await message.answer(texts["help_sent"], reply_markup=get_main_kb(lang))
    await state.set_state(None)


async def main():
    print("🤖 Launching Astana Guide Bot Service Engine running perfectly...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())