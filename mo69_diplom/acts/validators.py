"""
Валидатор XML файлов для форм КС-2/КС-3.
Проверяет соответствие XSD схеме.
"""

from lxml import etree
import os


def validate_xml(xml_content, schema_path=None):
    """
    Валидирует XML файл по XSD схеме.
    
    Args:
        xml_content: строка с XML содержимым
        schema_path: путь к XSD схеме (по умолчанию используется схема ks2_diadoc_schema.xsd)
    
    Returns:
        dict: результат валидации {'valid': bool, 'errors': list}
    """
    if schema_path is None:
        # Путь к схеме по умолчанию
        base_dir = os.path.dirname(os.path.abspath(__file__))
        schema_path = os.path.join(base_dir, 'schemas', 'ks2_diadoc_schema.xsd')
    
    result = {
        'valid': False,
        'errors': [],
        'warnings': []
    }
    
    try:
        # Парсим XML
        xml_doc = etree.fromstring(xml_content.encode('utf-8'))
        
        # Проверяем существование схемы
        if not os.path.exists(schema_path):
            result['warnings'].append(f'Файл схемы не найден: {schema_path}')
            result['valid'] = True  # Без схемы считаем валидным
            return result
        
        # Загружаем схему
        with open(schema_path, 'rb') as f:
            schema_doc = etree.parse(f)
        
        schema = etree.XMLSchema(schema_doc)
        
        # Валидируем
        if schema.validate(xml_doc):
            result['valid'] = True
        else:
            result['valid'] = False
            for error in schema.error_log:
                result['errors'].append({
                    'line': error.line,
                    'column': error.column,
                    'message': error.message,
                    'level': error.level_name
                })
    
    except etree.XMLSyntaxError as e:
        result['valid'] = False
        result['errors'].append({
            'line': e.lineno,
            'column': e.position[0] if len(e.position) > 0 else 0,
            'message': str(e),
            'level': 'ERROR'
        })
    except Exception as e:
        result['valid'] = False
        result['errors'].append({
            'message': str(e),
            'level': 'ERROR'
        })
    
    return result


def validate_xml_file(file_path, schema_path=None):
    """
    Валидирует XML файл по XSD схеме.
    
    Args:
        file_path: путь к XML файлу
        schema_path: путь к XSD схеме
    
    Returns:
        dict: результат валидации
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            xml_content = f.read()
        return validate_xml(xml_content, schema_path)
    except Exception as e:
        return {
            'valid': False,
            'errors': [{'message': str(e), 'level': 'ERROR'}],
            'warnings': []
        }
