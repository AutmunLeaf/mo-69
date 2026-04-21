"""
Генератор XML файлов для форм КС-2 и КС-3.
Формат соответствует Приказу ФНС № ЕД-7-26/691.
"""

from datetime import datetime
from decimal import Decimal


def generate_ks2_xml(act, items):
    """
    Генерирует XML файл для акта КС-2.
    
    Args:
        act: Объект модели Act
        items: queryset строк акта ActItem
    
    Returns:
        str: XML содержимое в кодировке windows-1251
    """
    contractor = act.contract.contractor
    contract = act.contract
    obj = act.object
    
    # Форматируем суммы
    total_amount = str(act.total_amount)
    nds_amount = str(act.nds_amount)
    
    xml = f'''<?xml version="1.0" encoding="windows-1251"?>
<Файл ВерсФорм="5.07" ВерсПрог="1.0.0" xmlns="http://www.nalog.ru/ndfl-document/" xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <Документ ИдДок="KS2-{act.number}-{act.date.strftime('%Y%m%d')}" ДатаДок="{act.date.strftime('%d.%m.%Y')}" ВремяДок="{datetime.now().strftime('%H:%M:%S')}">
    <КС2>
      <Заголовок>
        <НаимОргЗаказчик>{contract.contractor.name}</НаимОргЗаказчик>
        <ИННЗаказчик>{contractor.inn}</ИННЗаказчик>
        <КППЗаказчик>{contractor.kpp or ''}</КППЗаказчик>
        <НаимОргПодрядчик>{contractor.name}</НаимОргПодрядчик>
        <ИННПодрядчик>{contractor.inn}</ИННПодрядчик>
        <КПППодрядчик>{contractor.kpp or ''}</КПППодрядчик>
        <НомерДоговор>{contract.number}</НомерДоговор>
        <ДатаДоговор>{contract.date.strftime('%d.%m.%Y')}</ДатаДоговор>
        <НомерАкт>{act.number}</НомерАкт>
        <ДатаАкт>{act.date.strftime('%d.%m.%Y')}</ДатаАкт>
        <ПериодС>{act.period_start.strftime('%d.%m.%Y') if act.period_start else ''}</ПериодС>
        <ПериодПо>{act.period_end.strftime('%d.%m.%Y') if act.period_end else ''}</ПериодПо>
        <НаимОбъект>{obj.name}</НаимОбъект>
        <АдресОбъект>{obj.address or ''}</АдресОбъект>
      </Заголовок>
      <Таблица>
        <СуммаВсего>{total_amount}</СуммаВсего>
        <ВТомЧислеНДС>{nds_amount}</ВТомЧислеНДС>
        <БезНДС>{'true' if act.without_nds else 'false'}</БезНДС>
'''
    
    # Добавляем строки работ
    for i, item in enumerate(items, 1):
        item_total = str(item.total)
        item_price = str(item.price)
        item_quantity = str(item.quantity)
        
        xml += f'''        <Строка>
          <НомерПп>{item.number}</НомерПп>
          <НаименованиеРабот>{item.name}</НаименованиеРабот>
          <ЕдИзмерения>{item.unit}</ЕдИзмерения>
          <Количество>{item_quantity}</Количество>
          <Цена>{item_price}</Цена>
          <Стоимость>{item_total}</Стоимость>
        </Строка>
'''
    
    xml += f'''      </Таблица>
      <Подписант>
        <ФИОПодрядчик>{contractor.director_name or ''}</ФИОПодрядчик>
        <ДолжностьПодрядчик>{contractor.director_position or ''}</ДолжностьПодрядчик>
      </Подписант>
    </КС2>
  </Документ>
</Файл>'''
    
    return xml.encode('windows-1251').decode('windows-1251')


def generate_ks3_xml(act, items):
    """
    Генерирует XML файл для справки КС-3.
    
    Args:
        act: Объект модели Act
        items: queryset строк акта ActItem
    
    Returns:
        str: XML содержимое в кодировке windows-1251
    """
    contractor = act.contract.contractor
    contract = act.contract
    obj = act.object
    
    total_amount = str(act.total_amount)
    nds_amount = str(act.nds_amount)
    
    xml = f'''<?xml version="1.0" encoding="windows-1251"?>
<Файл ВерсФорм="5.07" ВерсПрог="1.0.0" xmlns="http://www.nalog.ru/ndfl-document/">
  <Документ ИдДок="KS3-{act.number}-{act.date.strftime('%Y%m%d')}" ДатаДок="{act.date.strftime('%d.%m.%Y')}" ВремяДок="{datetime.now().strftime('%H:%M:%S')}">
    <КС3>
      <Заголовок>
        <НаимОргЗаказчик>{contract.contractor.name}</НаимОргЗаказчик>
        <ИННЗаказчик>{contractor.inn}</ИННЗаказчик>
        <КППЗаказчик>{contractor.kpp or ''}</КППЗаказчик>
        <НаимОргПодрядчик>{contractor.name}</НаимОргПодрядчик>
        <ИННПодрядчик>{contractor.inn}</ИННПодрядчик>
        <КПППодрядчик>{contractor.kpp or ''}</КПППодрядчик>
        <НомерДоговор>{contract.number}</НомерДоговор>
        <ДатаДоговор>{contract.date.strftime('%d.%m.%Y')}</ДатаДоговор>
        <НомерАкт>{act.number}</НомерАкт>
        <ДатаАкт>{act.date.strftime('%d.%m.%Y')}</ДатаАкт>
        <НаимОбъект>{obj.name}</НаимОбъект>
        <АдресОбъект>{obj.address or ''}</АдресОбъект>
      </Заголовок>
      <Сведения>
        <СтоимостьРабот>{total_amount}</СтоимостьРабот>
        <НДС>{nds_amount}</НДС>
        <СтавкаНДС>{act.nds_rate}</СтавкаНДС>
        <БезНДС>{'true' if act.without_nds else 'false'}</БезНДС>
      </Сведения>
      <Подписант>
        <ФИОПодрядчик>{contractor.director_name or ''}</ФИОПодрядчик>
        <ДолжностьПодрядчик>{contractor.director_position or ''}</ДолжностьПодрядчик>
      </Подписант>
    </КС3>
  </Документ>
</Файл>'''
    
    return xml.encode('windows-1251').decode('windows-1251')
