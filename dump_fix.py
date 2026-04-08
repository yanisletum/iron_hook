import os
import django
import sys
from django.core import management

# 1. Добавляем текущую директорию в путь поиска модулей
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# 2. Автоматически ищем папку, где лежит settings.py
# Мы переберем папки и найдем ту, в которой есть settings.py
settings_module = None
for root, dirs, files in os.walk(current_dir):
    if 'settings.py' in files:
        # Получаем имя папки (например, 'core' или 'config')
        project_name = os.path.basename(root)
        settings_module = f"{project_name}.settings"
        break

if not settings_module:
    print("Ошибка: Не удалось найти файл settings.py!")
    sys.exit()

print(f"Используем настройки из: {settings_module}")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
django.setup()

# 3. Выгружаем данные
try:
    with open('datadump.json', 'w', encoding='utf-8') as f:
        management.call_command('dumpdata', 
                                '--natural-foreign', 
                                '--natural-primary', 
                                exclude=['contenttypes', 'auth.Permission'], 
                                indent=4, 
                                stdout=f)
    print("Успех! Чистый datadump.json в кодировке UTF-8 создан.")
except Exception as e:
    print(f"Произошла ошибка при дампе: {e}")