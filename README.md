🎣 Iron Hook — платформа для электронной коммерции и блогов о рыбалке на основе искусственного интеллекта

Полнофункциональное веб-приложение на Django с автоматизированным конвейером обработки контента на основе ИИ для интернет-магазина и блога, посвященных рыбалке.

Показать изображение
Показать изображение
Показать изображение
Показать изображение
Показать изображение
Показать изображение

📌 Обзор
Iron Hook — это развернутая в производственной среде платформа электронной коммерции для рыболовной отрасли со встроенным автономным конвейером создания контента для блога . Система на основе искусственного интеллекта автоматически исследует темы, генерирует SEO-оптимизированные статьи и отправляет уведомления через Telegram — без необходимости ручного написания.

✨ Особенности
🛒 Электронная коммерция

Каталог товаров с категориями и фильтрами
Корзина покупок и управление заказами
Аутентификация пользователей и профили
Администрирование Django для управления магазином.

🤖 Конвейер разработки блога об ИИ (CrewAI + RAG)

Шесть последовательно работающих агентов искусственного интеллекта обрабатывают полный жизненный цикл контента:

Исследователь тем → Автор контента → SEO-оптимизатор → Редактор → Издатель → Уведомитель


Система RAG на базе ChromaDB — агенты извлекают контекст из базы знаний по рыболовству.
Локальное обучение по программе LLM через Ollama (mistral :7b ) — без затрат на API OpenAI, полная конфиденциальность данных.
Telegram-бот отправляет уведомления о публикации новых статей.
Автоматическое создание записей непосредственно в административной панели Django.


🏗️ Архитектура
┌─────────────────────────────────────────────────────┐
│                    Iron Hook                        │
│                                                     │
│  Django App          AI Pipeline                    │
│  ┌──────────┐        ┌─────────────────────────┐   │
│  │  Shop    │        │  CrewAI (6 Agents)       │   │
│  │  Blog    │◄───────│  + ChromaDB RAG          │   │
│  │  Users   │        │  + Ollama mistral:7b     │   │
│  │  Cart    │        │  + Telegram Notifier     │   │
│  └──────────┘        └─────────────────────────┘   │
│       │                                             │
│  PostgreSQL                                         │
└───────┼─────────────────────────────────────────────┘
        │
   Deployed on Amvera Cloud

🛠️ Технологический стек
СлойТехнологииБэкендDjango 4.x, Python 3.11База данныхPostgreSQLАгенты искусственного интеллектаCrewAIмагистр праваОллама (мистраль :7b ) — местныйВектор БДChromaDBУведомленияAPI бота TelegramВнешний интерфейсHTML, CSS, JavaScriptРазвертываниеAmvera Cloud

🚀 Начало работы
Предварительные требования

Python 3.11+
PostgreSQL
Ollama с установленным Mistral :7b

Установка
баш# Clone the repository
git clone https://github.com/yanisletum/iron_hook.git
cd iron_hook

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your DB credentials and Telegram token

# Apply migrations
python manage.py migrate

# Run development server
python manage.py runserver
Переменные окружающей среды
окружающая средаSECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:password@localhost/iron_hook
TELEGRAM_BOT_TOKEN=your-telegram-token
OLLAMA_HOST=http://localhost:11434

🤖 Запуск конвейера ИИ
баш# Make sure Ollama is running with mistral:7b
ollama run mistral:7b

# Run the blog content pipeline
python manage.py run_pipeline --topic "fishing tips"
Трубопровод будет:

Изучите эту тему, используя RAG и базу знаний по рыболовству.
Создайте полностью оптимизированную для SEO статью.
Сохраните это как черновик в административной панели Django.
Отправить уведомление в Telegram


📁 Структура проекта
iron_hook/
├── blog/          # AI-generated blog posts
├── shop/          # E-commerce product catalog
├── cart/          # Shopping cart logic
├── users/         # Authentication & profiles
├── core/          # Shared utilities
├── config/        # Django settings
├── templates/     # HTML templates
├── static/        # CSS, JS, images
└── amvera.yml     # Deployment config

🌐 Живая демонстрация
Размещено по адресу: iron-hook.amvera.io

👤 Автор
Янис Летум — Разработчик Python | Агенты искусственного интеллекта и энтузиасты LLM
Показать изображение

📄 Лицензия
Лицензия MIT — можете смело использовать это в качестве источника вдохновения для своих собственных проектов.
