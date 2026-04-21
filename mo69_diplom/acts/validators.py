"""
Валидаторы XML файлов для форм КС-2 и КС-3
"""

import os
from lxml import etree


def validate_xml(xml_content, schema_name):
    """
    Валидация XML по XSD схеме
    
    Args:
        xml_content: bytes или str с XML контентом
        schema_name: имя файла XSD схемы (например, 'ks2_schema.xsd')
    
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    try:
        # Определяем путь к схеме
        schema_path = os.path.join(
            os.path.dirname(__file__),
            'schemas',
            schema_name
        )
        
        # Проверяем существование файла схемы
        if not os.path.exists(schema_path):
            return False, f"Файл схемы не найден: {schema_path}"
        
        # Загружаем XSD схему
        with open(schema_path, 'rb') as f:
            schema_doc = etree.parse(f)
        
        schema = etree.XMLSchema(schema_doc)
        
        # Парсим XML контент
        if isinstance(xml_content, bytes):
            xml_doc = etree.fromstring(xml_content)
        else:
            xml_doc = etree.fromstring(xml_content.encode('utf-8'))
        
        # Валидируем XML
        if schema.validate(xml_doc):
            return True, "XML успешно прошел валидацию по схеме"
        else:
            # Формируем сообщение об ошибках
            errors = []
            for error in schema.error_log:
                errors.append(f"Строка {error.line}: {error.message}")
            
            error_message = "Ошибки валидации:\n" + "\n".join(errors)
            return False, error_message
            
    except etree.XMLSyntaxError as e:
        return False, f"Ошибка синтаксиса XML: {str(e)}"
    except etree.XMLSchemaError as e:
        return False, f"Ошибка схемы XSD: {str(e)}"
    except Exception as e:
        return False, f"Неизвестная ошибка при валидации: {str(e)}"
