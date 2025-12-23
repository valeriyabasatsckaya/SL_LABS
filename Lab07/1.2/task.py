try:
    with open('input.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    print("Файл input.txt найден.")
except FileNotFoundError:
    print("Файл input.txt не найден. Создаём пример...")
    sample_text = """Привет это тестовая строка
В этой строке есть предлинноеслово
Python программирование файлы строки"""
    with open('input.txt', 'w', encoding='utf-8') as f:
        f.write(sample_text)
    with open('input.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    print("Пример input.txt создан.")

# Находим самое длинное слово в каждой строке
def longest_word(line):
    words = line.split()
    if not words:
        return ""
    return max(words, key=len)

output_lines = []
for line in lines:
    clean_line = line.strip()
    word = longest_word(clean_line)
    output_lines.append(word)

# Записываем в output.txt
with open('output.txt', 'w', encoding='utf-8') as f:
    for word in output_lines:
        f.write(word + '\n')

print("Обработка завершена. Результат записан в output.txt.")
print("\nСодержимое output.txt:")
for word in output_lines:
    print(f"  • {word}")
