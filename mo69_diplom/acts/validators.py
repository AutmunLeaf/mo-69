"""
Валидаторы XML файлов для форм КС-2 и КС-3
Простая валидация структуры без XSD схем
"""

import xml.etree.ElementTree as ET


def validate_xml(xml_content, schema_name=None):
    """
    Валидация XML файла
    Возвращает: (is_valid: bool, message: str)
    """
    try:
        # Попытка распарсить XML
        if isinstance(xml_content, bytes):
            root = ET.fromstring(xml_content)
        else:
            root = ET.fromstring(xml_content.encode('utf-8'))
        
        # Проверка корневого элемента
        if root.tag != 'Файл':
            return False, "Ошибка: Корневой элемент должен быть 'Файл'"
        
        # Проверка обязательных атрибутов
        required_attrs = ['ИдФайл', 'ВерсПрог', 'ВерсФорм']
        for attr in required_attrs:
            if attr not in root.attrib:
                return False, f"Ошибка: Отсутствует атрибут '{attr}'"
        
        # Поиск элемента Документ
        doc = root.find('Документ')
        if doc is None:
            return False, "Ошибка: Отсутствует элемент 'Документ'"
        
        # Проверка КНД
        knd = doc.get('КНД')
        if not knd:
            return False, "Ошибка: Отсутствует код формы (КНД)"
        
        if knd not in ['1110335', '1110336']:
            return False, f"Ошибка: Неверный код формы КНД: {knd}"
        
        # Проверка наличия элементов работ (ищем внутри Документ)
        items = doc.findall('НаимИСт')
        if len(items) == 0:
            return False, "Ошибка: Отсутствуют элементы работ"
        
        # Проверка итоговых сумм
        vsego = doc.find('ВсегоАктОтч')
        if vsego is None:
            return False, "Ошибка: Отсутствует элемент с итоговыми суммами"
        
        if not vsego.get('SumAktObsch'):
            return False, "Ошибка: Отсутствует общая сумма акта"
        
        # Проверка подписанта
        podp = doc.find('ПодписантПодр')
        if podp is None:
            return False, "Ошибка: Отсутствует информация о подписанте"
        
        return True, "XML файл успешно прошел валидацию"
        
    except ET.ParseError as e:
        return False, f"Ошибка парсинга XML: {str(e)}"
    except Exception as e:
        return False, f"Ошибка валидации: {str(e)}"
