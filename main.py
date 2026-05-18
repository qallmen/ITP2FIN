import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from geopy.distance import geodesic

from notion_client import Client # Add this at the very top

# 1. SETUP
BOT_TOKEN = "8734845651:AAFdQWfsYT9XfM7JqqDpobcSMfYdSMRzsXo"
# Get this from the 'Connections' page we created earlier
NOTION_TOKEN = "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"
# Get this from your Notion Page URL
NOTION_PAGE_ID = "PASTE_YOUR_PAGE_ID_HERE"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
notion = Client(auth=NOTION_TOKEN) # Initializes Notion
# 2. DATA STORAGE
RESTAURANTS = [
    {"name": "Line Brew Astana", "desc": "One of the city’s most famous steakhouses. Known for premium meat, grilled dishes, and house beer.", "link": "https://2gis.kz/astana/search/Line%20Brew", "lat": 51.1491, "lon": 71.4241, "photo": "https://2gis.kz/astana/gallery/geo/70000001030035728/photoId/30258560193956857", "feeds": []},
    {"name": "Saksaul", "desc": "Classic Kazakh and Central Asian restaurant with traditional interior, plov, horse meat dishes, and shashlik.", "link": "https://2gis.kz/astana/search/Saksaul", "lat": 51.1272, "lon": 71.4334, "photo": "https://sxodim.com/uploads/posts/2023/05/15/original.jpg", "feeds": []},
    {"name": "Felice", "desc": "Upscale Italian restaurant with elegant atmosphere, pasta, seafood, and fine dining service.", "link": "https://2gis.kz/astana/search/Felice", "lat": 51.1250, "lon": 71.4250, "photo": "https://images.unsplash.com/photo-1559339352-11d035aa65de", "feeds": []},
    {"name": "The Kitchen", "desc": "Modern European restaurant popular for breakfasts, steaks, and business dinners.", "link": "https://2gis.kz/astana/search/The%20Kitchen", "lat": 51.1211, "lon": 71.4289, "photo": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4", "feeds": []},
    {"name": "Qazaq Gourmet", "desc": "Luxury modern Kazakh cuisine with national dishes presented in contemporary style.", "link": "https://2gis.kz/astana/search/Qazaq%20Gourmet", "lat": 51.1092, "lon": 71.4328, "photo": "https://qazaqgourmet.kz/img/gallery/1.jpg", "feeds": []},
    {"name": "Eternal sky (Вечное небо)", "desc": "Panoramic restaurant with skyline views and Asian-European menu.", "link": "https://2gis.kz/astana/search/Eternal%20sky", "lat": 51.1322, "lon": 71.4111, "photo": "https://images.unsplash.com/photo-1504674900247-0877df9cc836", "feeds": []},
    {"name": "On The Roof", "desc": "Rooftop restaurant known for atmosphere, cocktails, and city views.", "link": "https://2gis.kz/astana/search/On%20The%20Roof", "lat": 51.1280, "lon": 71.4310, "photo": "https://images.unsplash.com/photo-1533777857889-4be7c70b33f7", "feeds": []},
    {"name": "Kishlak", "desc": "Popular Uzbek restaurant with large portions, plov, and traditional Eastern cuisine.", "link": "https://2gis.kz/astana/search/Kishlak", "lat": 51.1550, "lon": 71.4100, "photo": "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b", "feeds": []},
    {"name": "GINZA ASTANA", "desc": "Luxury restaurant and lounge with stylish interior and nightlife atmosphere.", "link": "https://2gis.kz/astana/search/GINZA", "lat": 51.1100, "lon": 71.4400, "photo": "https://images.unsplash.com/photo-1550966842-28ca260840bc", "feeds": []},
    {"name": "Portofino", "desc": "Elegant Italian restaurant often chosen for celebrations and romantic dinners.", "link": "https://2gis.kz/astana/search/Portofino", "lat": 51.1400, "lon": 71.4200, "photo": "https://images.unsplash.com/photo-1515003197210-e0cd71810b5f", "feeds": []},
    {"name": "Restaurant FARHI", "desc": "Well-known local restaurant with Kazakh and European dishes.", "link": "https://2gis.kz/astana/search/FARHI", "lat": 51.1600, "lon": 71.4300, "photo": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0", "feeds": []},
    {"name": "Grand Hall Astana", "desc": "Large upscale restaurant for banquets, family events, and traditional cuisine.", "link": "https://2gis.kz/astana/search/Grand%20Hall", "lat": 51.1520, "lon": 71.4250, "photo": "https://images.unsplash.com/photo-1519225421980-715cb0215aed", "feeds": []},
    {"name": "Astana Nury", "desc": "Popular restaurant with live music and traditional Kazakh-style atmosphere.", "link": "https://2gis.kz/astana/search/Astana%20Nury", "lat": 51.1650, "lon": 71.4210, "photo": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5", "feeds": []},
    {"name": "Roastbeef", "desc": "Highly rated steakhouse with premium meat and modern interior.", "link": "https://2gis.kz/astana/search/Roastbeef", "lat": 51.1200, "lon": 71.4300, "photo": "https://images.unsplash.com/photo-1544025162-d76694265947", "feeds": []},
    {"name": "Take Eat Easy", "desc": "Modern café-restaurant known for breakfasts and international dishes.", "link": "https://2gis.kz/astana/search/Take%20Eat%20Easy", "lat": 51.1350, "lon": 71.4450, "photo": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085", "feeds": []},
    {"name": "La Rivière", "desc": "Luxury Italian and Mediterranean fine dining restaurant.", "link": "https://2gis.kz/astana/search/La%20Riviere", "lat": 51.1450, "lon": 71.4180, "photo": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4", "feeds": []},
    {"name": "Salter's", "desc": "One of the best steak restaurants in the city according to reviews.", "link": "https://2gis.kz/astana/search/Salters", "lat": 51.1050, "lon": 71.4350, "photo": "https://images.unsplash.com/photo-1532592391327-9c18fd842702", "feeds": []},
    {"name": "Daredzhani", "desc": "Popular Georgian restaurant with khinkali and khachapuri.", "link": "https://2gis.kz/astana/search/Daredzhani", "lat": 51.1300, "lon": 71.4400, "photo": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38", "feeds": []},
    {"name": "Mökki", "desc": "Premium Italian restaurant with modern Scandinavian-inspired interior.", "link": "https://2gis.kz/astana/search/Mokki", "lat": 51.1150, "lon": 71.4250, "photo": "https://images.unsplash.com/photo-1543007630-9710e4a00a20", "feeds": []},
    {"name": "Cafe Momona", "desc": "Top-rated sushi and Pan-Asian restaurant. Popular among younger visitors and families.", "link": "https://2gis.kz/astana/search/Momona", "lat": 51.1290, "lon": 71.4220, "photo": "https://images.unsplash.com/photo-1553621042-f6e147245754", "feeds": []},
]

LIBRARIES = [
    {"name": "National Academic Library", "desc": "The largest and most famous library in Astana. Modern architecture and study atmosphere near Baiterek.", "link": "https://2gis.kz/astana/search/National%20Academic%20Library", "lat": 51.1264, "lon": 71.4361, "photo": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da", "feeds": []},
    {"name": "NU library", "desc": "Modern academic library at Nazarbayev University. Excellent for research and quiet studying.", "link": "https://2gis.kz/astana/search/NU%20library", "lat": 51.0900, "lon": 71.3990, "photo": "https://images.unsplash.com/photo-1491841573634-28140fc7ced7", "feeds": []},
    {"name": "Yenu. B07-Nauchnaya Biblioteka", "desc": "Scientific library of L.N. Gumilyov ENU. Popular among students and researchers.", "link": "https://2gis.kz/astana/search/Yenu%20Library", "lat": 51.1600, "lon": 71.4600, "photo": "https://images.unsplash.com/photo-1507733632304-b7ad44fe8a20", "feeds": []},
    {"name": "M. O. Auezov Central Library", "desc": "One of the main public libraries in the city with reading halls.", "link": "https://2gis.kz/astana/search/Auezov%20Library", "lat": 51.1700, "lon": 71.4150, "photo": "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f", "feeds": []},
    {"name": "KAZGUU Library", "desc": "Well-equipped university library with strong legal and humanities resources.", "link": "https://2gis.kz/astana/search/KAZGUU%20Library", "lat": 51.1250, "lon": 71.3700, "photo": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570", "feeds": []},
    {"name": "Republican Scientific Library", "desc": "Focused on science, engineering, and technical materials.", "link": "https://2gis.kz/astana/search/Scientific%20Library", "lat": 51.1500, "lon": 71.4200, "photo": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da", "feeds": []},
    {"name": "Yelbasy Library", "desc": "Library and archive center connected to Kazakhstan’s modern history.", "link": "https://2gis.kz/astana/search/Yelbasy%20Library", "lat": 51.1200, "lon": 71.4500, "photo": "https://images.unsplash.com/photo-1512820790803-83ca734da794", "feeds": []},
    {"name": "Youth and Children Library", "desc": "Popular among students with educational programs.", "link": "https://2gis.kz/astana/search/Youth%20Library", "lat": 51.1350, "lon": 71.4300, "photo": "https://images.unsplash.com/photo-1526367790999-0150786686a2", "feeds": []},
    {"name": "A.Gaidar Children's Library", "desc": "One of the best-known children’s libraries in Astana.", "link": "https://2gis.kz/astana/search/Gaidar%20Library", "lat": 51.1680, "lon": 71.4100, "photo": "https://images.unsplash.com/photo-1529148482759-b35b25c5f217", "feeds": []},
    {"name": "№5 кітапханасы", "desc": "Well-rated neighborhood public library.", "link": "https://2gis.kz/astana/search/Library%205", "lat": 51.1100, "lon": 71.4300, "photo": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da", "feeds": []},
    {"name": "Mass Library №1", "desc": "Small but highly rated public library branch.", "link": "https://2gis.kz/astana/search/Library%201", "lat": 51.1750, "lon": 71.4050, "photo": "https://images.unsplash.com/photo-1512820790803-83ca734da794", "feeds": []},
    {"name": "Mass Library №12", "desc": "Community-focused library with educational activities.", "link": "https://2gis.kz/astana/search/Library%2012", "lat": 51.1420, "lon": 71.4200, "photo": "https://images.unsplash.com/photo-1526367790999-0150786686a2", "feeds": []},
    {"name": "Library for the Blind", "desc": "Specialized library for visually impaired readers.", "link": "https://2gis.kz/astana/search/Blind%20Library", "lat": 51.1600, "lon": 71.4000, "photo": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da", "feeds": []},
    {"name": "International Turkic Academy", "desc": "Research-oriented library focused on Turkic studies.", "link": "https://2gis.kz/astana/search/Turkic%20Academy", "lat": 51.1150, "lon": 71.4450, "photo": "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f", "feeds": []},
    {"name": "Astana Library System", "desc": "Part of Astana’s centralized public library network.", "link": "https://2gis.kz/astana/search/Library%20System", "lat": 51.1500, "lon": 71.4200, "photo": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570", "feeds": []},
    {"name": "Eagilik Books & Coffee", "desc": "Hybrid bookstore, café, and reading space popular for studying.", "link": "https://2gis.kz/astana/search/Eagilik", "lat": 51.1580, "lon": 71.4280, "photo": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb", "feeds": []},
    {"name": "American Corner", "desc": "English-language learning center inside the National Library.", "link": "https://2gis.kz/astana/search/American%20Corner", "lat": 51.1264, "lon": 71.4361, "photo": "https://images.unsplash.com/photo-1526367790999-0150786686a2", "feeds": []},
    {"name": "Korean Center Library", "desc": "Korean literature collection inside the National Library.", "link": "https://2gis.kz/astana/search/Korean%20Library", "lat": 51.1264, "lon": 71.4361, "photo": "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f", "feeds": []},
    {"name": "German Literature Hall", "desc": "Foreign-language reading hall inside the National Library.", "link": "https://2gis.kz/astana/search/German%20Library", "lat": 51.1264, "lon": 71.4361, "photo": "https://images.unsplash.com/photo-1512820790803-83ca734da794", "feeds": []},
    {"name": "Digital Hub Library", "desc": "Tech-focused space for digital learning.", "link": "https://2gis.kz/astana/search/Digital%20Library", "lat": 51.1300, "lon": 71.4300, "photo": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570", "feeds": []},
]

PARKS = [
    {"name": "Presidential Park", "desc": "One of the city’s most iconic parks with fountains and bike paths.", "link": "https://2gis.kz/astana/search/Presidential%20Park", "lat": 51.1172, "lon": 71.4485, "photo": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05", "feeds": []},
    {"name": "Astana Central Park", "desc": "Riverside city park with amusement rides and long walking paths.", "link": "https://2gis.kz/astana/search/Central%20Park", "lat": 51.1633, "lon": 71.4192, "photo": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e", "feeds": []},
    {"name": "Zheruyyq Park", "desc": "Peaceful park known for trees, sculptures, and family atmosphere.", "link": "https://2gis.kz/astana/search/Zheruyyq", "lat": 51.1600, "lon": 71.4700, "photo": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05", "feeds": []},
    {"name": "Zhetisu Park", "desc": "Modern themed park with fountains and decorative architecture.", "link": "https://2gis.kz/astana/search/Zhetisu", "lat": 51.1500, "lon": 71.4350, "photo": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e", "feeds": []},
    {"name": "Lovers Park", "desc": "Popular for couples near Khan Shatyr. Features flower beds.", "link": "https://2gis.kz/astana/search/Lovers%20Park", "lat": 51.1320, "lon": 71.4050, "photo": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05", "feeds": []},
    {"name": "Linear Park", "desc": "Long modern park ideal for jogging on the left bank.", "link": "https://2gis.kz/astana/search/Linear%20Park", "lat": 51.1200, "lon": 71.4350, "photo": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e", "feeds": []},
    {"name": "Triathlon Park", "desc": "Best park for sports, running, and cycling enthusiasts.", "link": "https://2gis.kz/astana/search/Triathlon%20Park", "lat": 51.1450, "lon": 71.4550, "photo": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05", "feeds": []},
    {"name": "Expo 2017 Park", "desc": "Futuristic walking space near the EXPO complex.", "link": "https://2gis.kz/astana/search/Expo%20Park", "lat": 51.0900, "lon": 71.4150, "photo": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e", "feeds": []},
    {"name": "Atatürk Park", "desc": "Elegant park with clean paths and quiet atmosphere.", "link": "https://2gis.kz/astana/search/Ataturk%20Park", "lat": 51.1650, "lon": 71.4150, "photo": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05", "feeds": []},
    {"name": "Bauyrzhan Momyshuly Park", "desc": "Large favorite with playgrounds and greenery.", "link": "https://2gis.kz/astana/search/Momyshuly%20Park", "lat": 51.1620, "lon": 71.4720, "photo": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e", "feeds": []},
    {"name": "Korean Garden", "desc": "Beautiful Asian-style garden area popular for photography.", "link": "https://2gis.kz/astana/search/Korean%20Garden", "lat": 51.1660, "lon": 71.4220, "photo": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05", "feeds": []},
    {"name": "Central Fountain", "desc": "Known for fountains and evening atmosphere in the center.", "link": "https://2gis.kz/astana/search/Fountain", "lat": 51.1680, "lon": 71.4250, "photo": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e", "feeds": []},
    {"name": "Square Charles de Gaulle", "desc": "Compact European-style square with seating.", "link": "https://2gis.kz/astana/search/Gaulle%20Square", "lat": 51.1450, "lon": 71.4320, "photo": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05", "feeds": []},
    {"name": "Akzhayik", "desc": "Quiet riverside zone for local recreation.", "link": "https://2gis.kz/astana/search/Akzhayik", "lat": 51.1850, "lon": 71.4050, "photo": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e", "feeds": []},
    {"name": "Botanical Garden", "desc": "The largest major green zone with greenhouses and lakes.", "link": "https://2gis.kz/astana/search/Botanical%20Garden", "lat": 51.1050, "lon": 71.4250, "photo": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05", "feeds": []},
    {"name": "Green Belt", "desc": "Massive forest-park project surrounding the city.", "link": "https://2gis.kz/astana/search/Green%20Belt", "lat": 51.0500, "lon": 71.4500, "photo": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e", "feeds": []},
    {"name": "Arai Park", "desc": "Historical name of Zhetisu Park, still used by locals.", "link": "https://2gis.kz/astana/search/Arai%20Park", "lat": 51.1500, "lon": 71.4350, "photo": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05", "feeds": []},
    {"name": "Student Park", "desc": "Popular among university students for outdoor studying.", "link": "https://2gis.kz/astana/search/Student%20Park", "lat": 51.1600, "lon": 71.4650, "photo": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e", "feeds": []},
    {"name": "River Embankment", "desc": "Long pedestrian area connecting major parks.", "link": "https://2gis.kz/astana/search/Embankment", "lat": 51.1700, "lon": 71.4200, "photo": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05", "feeds": []},
    {"name": "Family Park", "desc": "Family-oriented recreation space with playgrounds.", "link": "https://2gis.kz/astana/search/Family%20Park", "lat": 51.1350, "lon": 71.4800, "photo": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e", "feeds": []},
]

# 3. KEYBOARDS
main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="📍 Nearest Cool Place", request_location=True)],
    [KeyboardButton(text="🍴 Restaurants"), KeyboardButton(text="🌳 Parks")],
    [KeyboardButton(text="📚 Libraries"), KeyboardButton(text="👨‍💻 Developers")],
    [KeyboardButton(text="🆘 Need Help?")]
], resize_keyboard=True)

def get_nav_buttons(cat, idx, link):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗺 Open in 2GIS", url=link)],
        [InlineKeyboardButton(text="🚀 Send Map Location", callback_data=f"go_{cat}_{idx}")],
        [InlineKeyboardButton(text="✍️ Leave Feedback", callback_data=f"write_{cat}_{idx}")],
        [InlineKeyboardButton(text="➡️ Another one", callback_data=f"next_{cat}_{idx}")]
    ])

# 4. CORE FUNCTION
async def send_place(target, cat, idx):
    db = {"rest": RESTAURANTS, "park": PARKS, "lib": LIBRARIES}[cat]
    item = db[idx % len(db)]

    feed_str = "\n".join([f"• {f}" for f in item['feeds']])
    text = (f"📍 **{item['name']}**\n\n"
            f"{item['desc']}\n\n"
            f"💬 **User Feedback:**\n{feed_str if feed_str else 'No feedback yet! Become the first.'}")

    kb = get_nav_buttons(cat, idx, item['link'])

    if isinstance(target, types.CallbackQuery):
        try:
            await target.message.delete()
        except:
            pass
        target_msg = target.message
    else:
        target_msg = target

    try:
        await target_msg.answer_photo(photo=item['photo'], caption=text, reply_markup=kb, parse_mode="Markdown")
    except Exception as e:
        print(f"Photo error: {e}")
        await target_msg.answer(text + "\n\n*(Photo unavailable)*", reply_markup=kb, parse_mode="Markdown")

# 5. HANDLERS
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Welcome to Astana Guide! How can I help you? 😊", reply_markup=main_kb)

@dp.message(F.text == "🆘 Need Help?")
async def help_init(message: types.Message, state: FSMContext):
    await message.answer("Please describe your problem. Our team will review it!")
    await state.set_state(BotStates.waiting_for_help)

@dp.message(BotStates.waiting_for_help)
async def help_received(message: types.Message, state: FSMContext):
    print(f"!!! ALERT !!! Problem from @{message.from_user.username}: {message.text}")
    await message.answer(f"Thank you for your feedback! Our developers ({ADMIN_HANDLES}) will contact you soon.")
    await state.clear()

@dp.message(F.text == "👨‍💻 Developers")
async def dev_info(message: types.Message):
    await message.answer(f"🚀 **Core Developers:**\n• @qallmen\n• @arabek127\n• @bzglnazerke\n\nNeed technical support? Click 'Need Help?'", reply_markup=main_kb)

@dp.message(F.text == "🍴 Restaurants")
async def start_rest(m: types.Message): await send_place(m, "rest", 0)

@dp.message(F.text == "🌳 Parks")
async def start_park(m: types.Message): await send_place(m, "park", 0)

@dp.message(F.text == "📚 Libraries")
async def start_lib(m: types.Message): await send_place(m, "lib", 0)

@dp.callback_query(F.data.startswith("next_"))
async def cb_next(call: types.CallbackQuery):
    _, cat, idx = call.data.split("_")
    await send_place(call, cat, int(idx) + 1)
    await call.answer()

@dp.callback_query(F.data.startswith("write_"))
async def cb_feed(call: types.CallbackQuery, state: FSMContext):
    _, cat, idx = call.data.split("_")
    await state.update_data(cat=cat, idx=idx)
    await call.message.answer(f"Please write your review for this place:")
    await state.set_state(BotStates.waiting_for_feedback)
    await call.answer()

@dp.message(BotStates.waiting_for_feedback)
async def feedback_saved(message: types.Message, state: FSMContext):
    data = await state.get_data()
    db = {"rest": RESTAURANTS, "park": PARKS, "lib": LIBRARIES}[data['cat']]
    # Save the feedback to the list
    db[int(data['idx']) % len(db)]['feeds'].append(message.text)
    await message.answer("Thank you for your feedback, it is valuable! ❤️")
    await state.clear()

@dp.callback_query(F.data.startswith("go_"))
async def cb_go(call: types.CallbackQuery):
    _, cat, idx = call.data.split("_")
    db = {"rest": RESTAURANTS, "park": PARKS, "lib": LIBRARIES}[cat]
    item = db[int(idx) % len(db)]
    await call.message.answer_location(latitude=item['lat'], longitude=item['lon'])
    await call.answer()

@dp.message(F.location)
async def handle_loc(m: types.Message):
    pos = (m.location.latitude, m.location.longitude)
    all_p = RESTAURANTS + PARKS + LIBRARIES
    near = min(all_p, key=lambda x: geodesic(pos, (x['lat'], x['lon'])).kilometers)
    await m.answer(f"🌟 **Nearest Recommended Place:**\n\n**{near['name']}**\n{near['desc']}", parse_mode="Markdown")
    await m.answer_location(latitude=near['lat'], longitude=near['lon'])

async def main():
    print("Astana Guide Bot Online...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())