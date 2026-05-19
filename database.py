import sqlite3

class DatabaseManager:
    def __init__(self, db_path='astana_bot.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
        self.seed_data_if_empty()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS places (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                name TEXT UNIQUE,
                description_en TEXT,
                description_kz TEXT,
                description_ru TEXT,
                rating TEXT,
                average_receipt TEXT,
                link_2gis TEXT,
                lat REAL,
                lon REAL,
                photo_url TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                place_name TEXT,
                feedback TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def add_review(self, place_name, feedback):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO reviews (place_name, feedback) VALUES (?, ?)", (place_name, feedback))
        self.conn.commit()

    def get_reviews_by_place(self, place_name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT feedback FROM reviews WHERE place_name = ?", (place_name,))
        return [row[0] for row in cursor.fetchall()]

    def get_places_by_category(self, category):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT name, description_en, description_kz, description_ru, rating, average_receipt, link_2gis, lat, lon, photo_url FROM places WHERE category = ?",
            (category,))
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_all_places(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, description_en, description_kz, description_ru, rating, average_receipt, link_2gis, lat, lon, photo_url FROM places")
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def seed_data_if_empty(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM places")
        if cursor.fetchone()[0] > 0:
            return

        restaurants = [
            ("Line Brew Astana", "Steakhouse, grills, premium meat", "Стейкхаус, гриль, премиум ет өнімдері", "Стейкхаус, гриль, премиум мясные блюда", "4.8", "15000 KZT", "https://2gis.kz/astana", 51.1605, 71.4242, "https://t.me/astana_bot_sbs/2"),
            ("Saksaul", "Traditional Kazakh cuisine", "Дәстүрлі қазақ тағамдары", "Традиционная казахская кухня", "4.7", "8000 KZT", "https://2gis.kz/astana", 51.1261, 71.4334, "https://t.me/astana_bot_sbs/3"),
            ("Qazaq Gourmet", "Modern Kazakh fine dining", "Заманауи қазақ жоғары асханасы", "Современная казахская высокая кухня", "4.9", "25000 KZT", "https://2gis.kz/astana", 51.1190, 71.4250, "https://t.me/astana_bot_sbs/4"),
            ("The Kitchen", "International cuisine", "Халықаралық асхана", "Интернациональная кухня", "4.5", "7000 KZT", "https://2gis.kz/astana", 51.1444, 71.4211, "https://t.me/astana_bot_sbs/5"),
            ("Roastbeef", "Steak & European menu", "Стейк және еуропалық мәзір", "Стейки и европейское меню", "4.6", "12000 KZT", "https://2gis.kz/astana", 51.1550, 71.4420, "https://t.me/astana_bot_sbs/6"),
            ("Wall Street", "Fusion / European", "Фьюжн / Еуропалық", "Фьюжн / Европейская", "4.4", "9000 KZT", "https://2gis.kz/astana", 51.1285, 71.4310, "https://t.me/astana_bot_sbs/7"),
            ("La Rivière", "Premium European dining", "Премиум еуропалық асхана", "Премиальная европейская кухня", "4.8", "20000 KZT", "https://2gis.kz/astana", 51.1640, 71.4190, "https://t.me/astana_bot_sbs/8"),
            ("MÖKKI", "Fine dining / Scandinavian style", "Талғампаз асхана / Скандинавиялық стиль", "Изысканная кухня / Скандинавский стиль", "4.7", "18000 KZT", "https://2gis.kz/astana", 51.1242, 71.4265, "https://t.me/astana_bot_sbs/9"),
            ("Zina", "Modern restaurant & brunch", "Заманауи мейрамхана және бранч", "Современный ресторан и бранч", "4.5", "6500 KZT", "https://2gis.kz/astana", 51.1390, 71.4150, "https://t.me/astana_bot_sbs/10"),
            ("Ocean Basket", "Seafood specialist chain", "Теңіз өнімдерінің мамандандырылған желісі", "Специализированная сеть морепродуктов", "4.6", "8500 KZT", "https://2gis.kz/astana", 51.1331, 71.4225, "https://t.me/astana_bot_sbs/11"),
            ("Cafestar", "European café-restaurant", "Еуропалық кафе-мейрамхана", "Европейское кафе-ресторан", "4.4", "6000 KZT", "https://2gis.kz/astana", 51.1270, 71.4340, "https://t.me/astana_bot_sbs/12"),
            ("Eternal sky", "Panoramic restaurant", "Панорамалық мейрамхана", "Панорамный ресторан", "4.7", "11000 KZT", "https://2gis.kz/astana", 51.1311, 71.4180, "https://t.me/astana_bot_sbs/13"),
            ("Cafe Momona", "Authentic Japanese cuisine", "Түпнұсқа жапон асханасы", "Аутентичная японская кухня", "4.5", "7500 KZT", "https://2gis.kz/astana", 51.1480, 71.4390, "https://t.me/astana_bot_sbs/14"),
            ("Felice", "Elegant Italian restaurant", "Талғампаз итальяндық мейрамхана", "Элегантный итальянский ресторан", "4.7", "13000 KZT", "https://2gis.kz/astana", 51.1210, 71.4290, "https://t.me/astana_bot_sbs/15"),
            ("NaNe Panasian", "Flavorful Pan-Asian cuisine", "Дәмді паназиялық асхана", "Насыщенная паназиатская кухня", "4.3", "5500 KZT", "https://2gis.kz/astana", 51.1590, 71.4610, "https://t.me/astana_bot_sbs/16"),
            ("Osoba", "Rich Georgian cuisine", "Бай грузин асханасы", "Насыщенная грузинская кухня", "4.6", "7000 KZT", "https://2gis.kz/astana", 51.1620, 71.4280, "https://t.me/astana_bot_sbs/17"),
            ("Focaccia", "Pizza & classic Italian", "Пицца және классикалық итальяндық", "Пицца и классическая итальянская кухня", "4.5", "5000 KZT", "https://2gis.kz/astana", 51.1150, 71.4080, "https://t.me/astana_bot_sbs/18"),
            ("Monte Bianco", "European comfort food", "Еуропалық жайлы тағамдар", "Европейская домашняя кухня", "4.2", "6500 KZT", "https://2gis.kz/astana", 51.1277, 71.4366, "https://t.me/astana_bot_sbs/19"),
            ("Nasha Dacha", "Cozy Country-style restaurant", "Шығыс стиліндегі жайлы мейрамхана", "Уютный ресторан загородного стиля", "4.6", "9500 KZT", "https://2gis.kz/astana", 51.1820, 71.4010, "https://t.me/astana_bot_sbs/20"),
            ("Mari", "Italian & European bistro", "Итальяндық және еуропалық бистро", "Итальянское и европейское бистро", "4.5", "8000 KZT", "https://2gis.kz/astana", 51.1350, 71.4270, "https://t.me/astana_bot_sbs/21")
        ]

        parks = [
            ("Astana Central Park", "Oldest park along the Ishim River with attractions.", "Есіл өзенінің бойындағы аттракциондары бар ең ескі саябақ.", "Старейший парк вдоль реки Есиль с аттракционами.", "4.6", "Free Entry", "https://2gis.kz/astana", 51.1632, 71.4145, "https://t.me/astana_bot_sbs/22"),
            ("Presidential Park", "Massive green park near Ak Orda with beautiful fountains.", "Ақорданың жанындағы әдемі субұрқақтары бар үлкен жасыл саябақ.", "Огромный зеленый парк возле Ак Орды с красивыми фонтанами.", "4.5", "Free Entry", "https://2gis.kz/astana", 51.1245, 71.4485, "https://t.me/astana_bot_sbs/23"),
            ("Zheruyyq Park", "Beautiful landscaped park with thousands of trees.", "Мыңдаған ағаштары бар әдемі абаттандырылған саябақ.", "Красивый благоустроенный парк с тысячами деревьев.", "4.4", "Free Entry", "https://2gis.kz/astana", 51.1561, 71.4722, "https://t.me/astana_bot_sbs/24"),
            ("Zhetisu Park", "Modern thematic park inspired by Zhetysu region.", "Жетісу өңірінің стиліндегі заманауи тақырыптық саябақ.", "Современный тематический парк в стиле Жетысуского региона.", "4.7", "Free Entry", "https://2gis.kz/astana", 51.1382, 71.4410, "https://t.me/astana_bot_sbs/25"),
            ("Lovers Park", "Romantic urban park right near Khan Shatyr.", "Хан Шатырдың жанындағы романтикалық қалалық саябақ.", "Романтический городской парк прямо возле Хан Шатыра.", "4.6", "Free Entry", "https://2gis.kz/astana", 51.1305, 71.4032, "https://t.me/astana_bot_sbs/26"),
            ("Linear Park", "Long modern pedestrian corridor on the left bank.", "Сол жағалаудағы ұзын заманауи жаяу жүргіншілер дәлізі.", "Длинный современный пешеходный коридор на левом берегу.", "4.6", "Free Entry", "https://2gis.kz/astana", 51.1250, 71.4210, "https://t.me/astana_bot_sbs/27"),
            ("Triathlon Park", "Sports-oriented park popular among runners.", "Жүгірушілер арасында танымал спорттық саябақ.", "Спортивный парк, популярный среди бегунов.", "4.7", "Free Entry", "https://2gis.kz/astana", 51.1490, 71.4450, "https://t.me/astana_bot_sbs/28"),
            ("Atatürk Park", "Compact, very clean, and calm neighborhood park.", "Шағын, өте таза және тыныш аудандық саябақ.", "Компактный, очень чистый и тихий районный парк.", "4.8", "Free Entry", "https://2gis.kz/astana", 51.1620, 71.4310, "https://t.me/astana_bot_sbs/29"),
            ("Bauyrzhan Momyshuly Park", "Large public park with playgrounds.", "Ойын алаңдары бар үлкен қоғамдық саябақ.", "Большой общественный парк с игровыми площадками.", "4.5", "Free Entry", "https://2gis.kz/astana", 51.1520, 71.4650, "https://t.me/astana_bot_sbs/30"),
            ("Expo 2017 park", "Modern landscaped park near EXPO complex.", "ЭКСПО кешенінің жанындағы заманауи ландшафты саябақ.", "Современный ландшафтный парк возле комплекса ЭКСПО.", "4.6", "Free Entry", "https://2gis.kz/astana", 51.0910, 71.4180, "https://t.me/astana_bot_sbs/31"),
            ("Peace and Unity Alley", "Peaceful alley-park area near the Pyramid.", "Пирамиданың жанындағы тыныш аллея-саябақ аймағы.", "Спокойная аллея-парковая зона возле Пирамиды.", "4.6", "Free Entry", "https://2gis.kz/astana", 51.1220, 71.4440, "https://t.me/astana_bot_sbs/32"),
            ("Park of the Birches", "Small but scenic natural-style park.", "Шағын, бірақ әдемі табиғи стильдегі саябақ.", "Небольшой, но живописный парк в природном стиле.", "4.9", "Free Entry", "https://2gis.kz/astana", 51.1710, 71.4550, "https://t.me/astana_bot_sbs/33"),
            ("Central Fountain", "Popular city relaxation area.", "Қала тұрғындарының танымал демалыс орны.", "Популярное городское место отдыха.", "4.7", "Free Entry", "https://2gis.kz/astana", 51.1610, 71.4190, "https://t.me/astana_bot_sbs/34"),
            ("Botanical Garden", "Largest botanical park with beautiful lakes.", "Әдемі көлдері бар ең үлкен ботаникалық саябақ.", "Самый большой ботанический парк с красивыми озерами.", "4.8", "Free Entry", "https://2gis.kz/astana", 51.1110, 71.4150, "https://t.me/astana_bot_sbs/35"),
            ("Green Belt Park", "Eco-project forest belt around the city limits.", "Қала шетіндегі эко-жоба ормандар белдеуі.", "Лесной пояс эко-проекта вокруг городской черты.", "4.5", "Free Entry", "https://2gis.kz/astana", 51.0500, 71.3800, "https://t.me/astana_bot_sbs/36"),
            ("Family Park Astana", "Family-oriented setup with playgrounds.", "Ойын алаңдары бар отбасылық демалыс орны.", "Семейное пространство с игровыми площадками.", "4.3", "Free Entry", "https://2gis.kz/astana", 51.1420, 71.4810, "https://t.me/astana_bot_sbs/37"),
            ("River Embankment Park", "Long riverside walking strip with skyline views.", "Қала көрінісі бар өзен бойындағы ұзын серуендеу аймағы.", "Длинная набережная для прогулок с красивым видом.", "4.7", "Free Entry", "https://2gis.kz/astana", 51.1680, 71.4110, "https://t.me/astana_bot_sbs/37"),
            ("Student Park", "Calm green area near universities.", "Университеттер жанындағы тыныш жасыл аймақ.", "Спокойная зеленая зона возле университетов.", "4.3", "Free Entry", "https://2gis.kz/astana", 51.1550, 71.4990, "https://t.me/astana_bot_sbs/39"),
            ("Akbulak Riverside", "Riverside zone with modern urban configurations.", "Заманауи қалалық инфрақұрылымы бар өзен жағалауы.", "Прибрежная зона с современной городской застройкой.", "4.5", "Free Entry", "https://2gis.kz/astana", 51.1510, 71.4520, "https://t.me/astana_bot_sbs/40")
        ]

        libraries = [
            ("National Academic Library", "One of the largest libraries in KZ with 32 halls.", "32 залы бар Қазақстандағы ең үлкен кітапханалардың бірі.", "Одна из крупнейших библиотек в РК с 32 залами.", "4.9", "Free Access", "https://2gis.kz/astana", 51.1275, 71.4241, "https://t.me/astana_bot_sbs/41"),
            ("NU Library", "Main library of Nazarbayev University.", "Назарбаев Университетінің басты кітапханасы.", "Главная библиотека Назарбаев Университета.", "4.9", "Students/Permit", "https://2gis.kz/astana", 51.0905, 71.3985, "https://t.me/astana_bot_sbs/42"),
            ("M. O. Auezov Library", "Historic public library offering reading halls.", "Оқу залдары бар тарихи қоғамдық кітапхана.", "Историческая публичная библиотека с читальными залами.", "4.5", "Free Access", "https://2gis.kz/astana", 51.1690, 71.4280, "https://t.me/astana_bot_sbs/43"),
            ("KAZGUU Library", "Academic library focusing on legal assets.", "Құқықтық ресурстарға бағытталған академиялық кітапхана.", "Академическая библиотека с юридическим уклоном.", "4.6", "Students/Permit", "https://2gis.kz/astana", 51.1180, 71.3690, "https://t.me/astana_bot_sbs/44"),
            ("Scientific Library", "Specialized tech library serving STEM requirements.", "STEM бағытына арналған мамандандырылған техникалық кітапхана.", "Специализированная техническая библиотека для STEM.", "4.4", "Free Access", "https://2gis.kz/astana", 51.1420, 71.4320, "https://t.me/astana_bot_sbs/45"),
            ("Central Youth Library", "Children and youth literary configuration.", "Балалар мен жастарға арналған әдебиет орталығы.", "Детско-юношеский литературный центр.", "4.5", "Free Access", "https://2gis.kz/astana", 51.1510, 71.4110, "https://t.me/astana_bot_sbs/46"),
            ("Eagilik Books & Coffee", "Cozy coffeehouse setting mixed with study resources.", "Оқу ресурстарымен біріктірілген жайлы кофехана.", "Уютная кофейня с книжным фондом для обучения.", "4.8", "Purchase Based", "https://2gis.kz/astana", 51.1622, 71.4215, "https://t.me/astana_bot_sbs/47"),
            ("Biblioteka Nezryachikh", "Specialized setup for visually impaired readers.", "Көру қабілеті бұзылған оқырмандарға арналған арнайы кітапхана.", "Специализированная библиотека для незрячих.", "4.7", "Free Access", "https://2gis.kz/astana", 51.1710, 71.3910, "https://t.me/astana_bot_sbs/48"),
            ("Prezident Library", "Archives mapping historical development items.", "Тарихи даму мұрағаттары жинақталған орын.", "Архивные материалы исторического развития.", "4.6", "Free Access", "https://2gis.kz/astana", 51.1210, 71.4420, "https://t.me/astana_bot_sbs/49"),
            ("Turkic Academy", "Research library focused on Turkic studies.", "Түркітану зерттеулеріне бағытталған ғылыми кітапхана.", "Исследовательская библиотека тюркологии.", "4.7", "Research Permit", "https://2gis.kz/astana", 51.1195, 71.4390, "https://t.me/astana_bot_sbs/50"),
            ("Kitapkhana 5", "Local community library asset.", "Жергілікті қауымдастыққа арналған кітапхана.", "Местная районная библиотека.", "4.1", "Free Access", "https://2gis.kz/astana", 51.1810, 71.4410, "https://t.me/astana_bot_sbs/51"),
            ("Massovaya 1", "Neighborhood public library serving old center.", "Ескі орталыққа қызмет көрсететін халықтық кітапхана.", "Публичная библиотека, обслуживающая старый центр.", "4.2", "Free Access", "https://2gis.kz/astana", 51.1720, 71.4190, "https://images.unsplash.com/photo-1529148482759-b35b25c5f217?q=80&w=600"),
            ("Massovaya 12", "Local district branch supporting general fiction.", "Көркем әдебиетті қолдайтын жергілікті бөлімше.", "Районный филиал с художественной литературой.", "4.0", "Free Access", "https://2gis.kz/astana", 51.1390, 71.4720, "https://images.unsplash.com/photo-1526244433442-722770a5275c?q=80&w=600"),
            ("Massovaya General", "Public reading asset for regional citizens.", "Аймақ тұрғындарына арналған қоғамдық оқу орны.", "Публичное пространство для чтения граждан.", "4.1", "Free Access", "https://2gis.kz/astana", 51.1550, 71.4480, "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?q=80&w=600"),
            ("Massovaya 2", "District library providing classic works.", "Классикалық шығармаларды ұсынатын аудандық кітапхана.", "Районная библиотека с классическими трудами.", "4.2", "Free Access", "https://2gis.kz/astana", 51.1610, 71.4620, "https://images.unsplash.com/photo-1506880018603-83d5b814b5a6?q=80&w=600"),
            ("Centralized System", "Headquarters uniting 25 library arrays.", "25 кітапхана жүйесін біріктіретін бас кеңсе.", "Штаб-квартира, объединяющая 25 библиотек.", "4.5", "Free Access", "http://astana-library.kz", 51.1490, 71.4220, "https://images.unsplash.com/photo-1457369804613-52c61a468e7d?q=80&w=600"),
            ("American Corner", "English resource asset inside National library.", "Ұлттық кітапхана ішіндегі ағылшын тілі ресурстары орталығы.", "Центр английских ресурсов внутри Национальной библиотеки.", "4.8", "Free Access", "https://2gis.kz/astana", 51.1275, 71.4241, "https://t.me/astana_bot_sbs/52"),
            ("Museum of Book", "Rare printings and historic publishing assets.", "Сирек кездесетін басылымдар мен тарихи кітаптар мұражайы.", "Музей редких печатных изданий и исторических книг.", "4.7", "Free Access", "https://2gis.kz/astana", 51.1275, 71.4241, "https://t.me/astana_bot_sbs/53"),
            ("Electronic Library", "KAZNEB operational physical station.", "ҚАЗҰЭК цифрлық мұрағаттау станциясы.", "Физическая станция цифрового архивирования КАЗНЭБ.", "4.6", "Online/Free", "http://kazneb.kz", 51.1275, 71.4241, "https://t.me/astana_bot_sbs/54")
        ]

        for row in restaurants:
            cursor.execute("INSERT OR IGNORE INTO places (category, name, description_en, description_kz, description_ru, rating, average_receipt, link_2gis, lat, lon, photo_url) VALUES ('rest', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row)
        for row in parks:
            cursor.execute("INSERT OR IGNORE INTO places (category, name, description_en, description_kz, description_ru, rating, average_receipt, link_2gis, lat, lon, photo_url) VALUES ('park', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row)
        for row in libraries:
            cursor.execute("INSERT OR IGNORE INTO places (category, name, description_en, description_kz, description_ru, rating, average_receipt, link_2gis, lat, lon, photo_url) VALUES ('lib', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row)

        self.conn.commit()