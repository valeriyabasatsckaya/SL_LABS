import requests
import json
import os

# Конфигурация для поиска западноафриканских стран
SUBREGION = 'Western Africa'
POPULATION_THRESHOLD = 10_000_000


def fetch_countries_data():
    """Получает список стран по субрегиону через API"""
    api_url = f'https://restcountries.com/v3.1/subregion/{SUBREGION}'
    params = {
        "fields": "name,capital,area,population,borders,flags,flag,cca2"
    }
    try:
        resp = requests.get(api_url, params=params)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as error:
        print(f'Не удалось загрузить данные: {error}')
        return []


def filter_by_population(countries_list, min_population):
    """Фильтрует страны по минимальному населению"""
    filtered_list = []
    for country in countries_list:
        country_population = country.get('population', 0)
        if country_population > min_population:
            filtered_list.append(country)
    return filtered_list


def save_flag_image(image_url, country_title, suffix):
    """Скачивает и сохраняет флаг страны"""
    try:
        image_data = requests.get(image_url)
        image_data.raise_for_status()
        
        # Создаём папку для флагов
        if not os.path.exists('flags'):
            os.makedirs('flags')
        
        # Формируем безопасное имя файла
        clean_name = country_title.replace(' ', '_').replace('/', '_')
        filename = f'flags/{clean_name}_{suffix}.png'
        
        with open(filename, 'wb') as file:
            file.write(image_data.content)
        
        return filename
    except Exception as err:
        print(f'Ошибка сохранения флага: {err}')
        return None


def get_flag_url_by_iso(country):
    """Получает URL флага по ISO-коду"""
    iso_code = country.get('cca2')
    if iso_code:
        return f"https://flagcdn.com/w320/{iso_code.lower()}.png"
    return None


def get_flag_url_by_emoji(country):
    """Получает URL флага по эмодзи"""
    emoji = country.get('flag')
    if emoji and len(emoji) >= 2:
        # Извлекаем ISO-код из эмодзи
        base = ord('🇦') - ord('A')
        chars = [chr(ord(char) - 0x1F1A5) for char in emoji if char.isalpha()]
        iso_code = ''.join(chars)
        if len(iso_code) == 2:
            return f"https://flagcdn.com/w320/{iso_code.lower()}.png"
    return None


def parse_country_data(country_obj):
    """Извлекает нужную информацию о стране"""
    country_dict = {}
    
    # Получаем название
    name_data = country_obj.get('name', {})
    country_dict['name'] = name_data.get('common', 'Неизвестно')
    
    # Получаем столицу
    capitals = country_obj.get('capital', [])
    country_dict['capital'] = capitals[0] if capitals else 'Неизвестно'
    
    # Площадь и население
    country_dict['area'] = country_obj.get('area', 0)
    country_dict['population'] = country_obj.get('population', 0)
    
    # Список соседей
    borders = country_obj.get('borders', [])
    country_dict['borders'] = borders
    country_dict['border_count'] = len(borders)
    
    # URL флага
    flag_url = get_flag_url_by_emoji(country_obj) or get_flag_url_by_iso(country_obj)
    country_dict['flag_url'] = flag_url
    
    return country_dict


def find_top_countries_by_borders(countries_list, n=3):
    """Находит топ-N стран по количеству соседей"""
    sorted_countries = sorted(countries_list, key=lambda x: x['border_count'], reverse=True)
    return sorted_countries[:n]


def process_country_data():
    """Основная функция обработки данных"""
    print(f'\n--- Обработка: страны Западной Африки с населением > {POPULATION_THRESHOLD:,} ---')
    
    # Получаем все страны Западной Африки
    all_countries = fetch_countries_data()
    print(f'Найдено стран: {len(all_countries)}')
    
    # Фильтруем по населению
    large_countries = filter_by_population(all_countries, POPULATION_THRESHOLD)
    print(f'Подходящих по населению: {len(large_countries)}')
    
    parsed_countries = []
    
    # Обрабатываем каждую страну
    for country in large_countries:
        country_info = parse_country_data(country)
        parsed_countries.append(country_info)
    
    # Находим топ-3 по количеству соседей
    top_3 = find_top_countries_by_borders(parsed_countries)
    
    print(f'\nТоп-3 страны по числу соседей:')
    for country_info in top_3:
        print(f'→ {country_info["name"]}: {country_info["border_count"]} соседей')
    
    # Скачиваем флаги для топ-3
    for country_info in top_3:
        flag_url = country_info.get('flag_url')
        if flag_url:
            flag_file = save_flag_image(
                flag_url,
                country_info['name'],
                'flag'
            )
            if flag_file:
                print(f'✓ Флаг сохранён: {flag_file}')
        else:
            print(f'✗ Нет флага для {country_info["name"]}')
    
    with open('results.json', 'w', encoding='utf-8') as output_file:
        json.dump(parsed_countries, output_file, ensure_ascii=False, indent=2)
    
    print('\n' + '='*60)
    print('РЕЗУЛЬТАТЫ СОХРАНЕНЫ В results.json')
    print('ФЛАГИ СОХРАНЕНЫ В ПАПКУ flags/')
    print('='*60)


if __name__ == '__main__':
    process_country_data()