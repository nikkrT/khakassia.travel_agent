import json
import re

def extract_json(content):
    def try_parse(json_str):
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            # print(f"Ошибка при парсинге JSON: {e}\nContent:\n{json_str}")  # Для отладки
            return None

    # Удаляем обертки ```json ```
    content_cleaned = re.sub(r'^```(?:json)?\s*|\s*```$', '', content.strip(), flags=re.DOTALL)
    
    # Попытка 1: Парсим весь контент
    result = try_parse(content_cleaned)
    if result is not None:
        return result
    
    # Попытка 2: Ищем все JSON-блоки (без вложенных объектов)
    json_blocks = re.findall(r'(?s)\{.*?\}', content_cleaned)  # Упрощенное регулярное выражение
    if json_blocks:
        # Проверяем блоки в обратном порядке
        for block in reversed(json_blocks):
            result = try_parse(block)
            if result is not None:
                return result
    
    # Попытка 3: Ищем по последним скобкам
    last_open = content_cleaned.rfind('{')
    last_close = content_cleaned.rfind('}')
    if last_open != -1 and last_close > last_open:
        result = try_parse(content_cleaned[last_open:last_close+1])
        if result is not None:
            return result
    
    return content  # Возвращаем оригинал, если не найдено
