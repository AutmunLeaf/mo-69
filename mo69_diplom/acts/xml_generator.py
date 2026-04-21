"""
Генератор XML файлов для форм КС-2 и КС-3
Соответствует Приказу ФНС России № ЕД-7-26/691
Кодировка: Windows-1251
"""

from xml.etree.ElementTree import Element, SubElement, tostring
from datetime import datetime
import uuid


def generate_ks2_xml(act, items):
    """
    Генерация XML для формы КС-2
    """
    # Корневой элемент
    root = Element('Файл')
    root.set('ИдФайл', f"KS2-{act.id}-{uuid.uuid4().hex[:8].upper()}")
    root.set('ВерсПрог', '5.0')
    root.set('ВерсФорм', '5.0')
    
    # Документ
    doc = SubElement(root, 'Документ')
    doc.set('КНД', '1110335')  # Код формы КС-2
    doc.set('ДатаИнфПодр', act.created_at.strftime('%d.%m.%Y'))
    doc.set('ВремИнфПодр', act.created_at.strftime('%H:%M:%S'))
    doc.set('НаимЭкСубСост', 'ООО «Мостоотряд-69»')
    
    # Сведения об акте
    sv_act = SubElement(doc, 'СвАктСдПр')
    sv_act.set('НомАкт', str(act.number))
    sv_act.set('ДатаАкт', act.date.strftime('%d.%m.%Y'))
    sv_act.set('НаимСтр', act.object.name if act.object else '')
    if act.period_start:
        sv_act.set('ПериодС', act.period_start.strftime('%d.%m.%Y'))
    if act.period_end:
        sv_act.set('ПериодПо', act.period_end.strftime('%d.%m.%Y'))
    
    # Договор
    if act.contract:
        sv_act.set('НомДог', act.contract.number or '')
        if act.contract.date:
            sv_act.set('ДатаДог', act.contract.date.strftime('%d.%m.%Y'))
    
    # Элементы работ
    for idx, item in enumerate(items, 1):
        naim_ist = SubElement(doc, 'НаимИСт')
        naim_ist.set('НомСтр', str(idx))
        work_name = item.name or (item.work_type.name if item.work_type else '')
        naim_ist.set('НаимРабот', work_name)
        naim_ist.set('EdIzm', item.unit or 'ед.')
        naim_ist.set('Kolichestvo', str(item.quantity))
        naim_ist.set('TsenaEd', str(item.price))
        naim_ist.set('Stoimost', str(item.total))
    
    # Настройки формирования
    nastr = SubElement(doc, 'НастрФормДок')
    nastr.set('PrintFormat', 'XML')
    
    # Итоговые суммы
    vsego = SubElement(doc, 'ВсегоАктОтч')
    total_sum = sum(item.total for item in items)
    vsego.set('SumAktObsch', f"{total_sum:.2f}")
    
    # Подписант от подрядчика
    podp = SubElement(doc, 'ПодписантПодр')
    podp.set('DolzhnPodp', 'Генеральный директор')
    if act.contract and act.contract.contractor:
        podp.set('FIO', act.contract.contractor.name)
    else:
        podp.set('FIO', '________________')
    podp.set('DeystvNaOsn', 'Устава')
    
    # Преобразование в строку с кодировкой Windows-1251
    xml_str = tostring(root, encoding='windows-1251', xml_declaration=True)
    
    return xml_str


def generate_ks3_xml(act, items):
    """
    Генерация XML для формы КС-3
    """
    # Корневой элемент
    root = Element('Файл')
    root.set('ИдФайл', f"KS3-{act.id}-{uuid.uuid4().hex[:8].upper()}")
    root.set('ВерсПрог', '5.0')
    root.set('ВерсФорм', '5.0')
    
    # Документ
    doc = SubElement(root, 'Документ')
    doc.set('КНД', '1110336')  # Код формы КС-3
    doc.set('ДатаИнфПодр', act.created_at.strftime('%d.%m.%Y'))
    doc.set('ВремИнфПодр', act.created_at.strftime('%H:%M:%S'))
    doc.set('НаимЭкСубСост', 'ООО «Мостоотряд-69»')
    
    # Сведения о справке
    sv_spravka = SubElement(doc, 'СвSpravka')
    sv_spravka.set('НомСправ', str(act.number))
    sv_spravka.set('ДатаСправ', act.date.strftime('%d.%m.%Y'))
    sv_spravka.set('НаимСтр', act.object.name if act.object else '')
    
    # Договор
    if act.contract:
        sv_spravka.set('НомДог', act.contract.number or '')
        if act.contract.date:
            sv_spravka.set('ДатаДог', act.contract.date.strftime('%d.%m.%Y'))
    
    # Элементы работ
    for idx, item in enumerate(items, 1):
        naim_ist = SubElement(doc, 'НаимИСт')
        naim_ist.set('НомСтр', str(idx))
        work_name = item.name or (item.work_type.name if item.work_type else '')
        naim_ist.set('НаимРабот', work_name)
        naim_ist.set('Stoimost', str(item.total))
    
    # Настройки формирования
    nastr = SubElement(doc, 'НастрФормДок')
    nastr.set('PrintFormat', 'XML')
    
    # Итоговые суммы
    vsego = SubElement(doc, 'ВсегоАктОтч')
    total_sum = sum(item.total for item in items)
    vsego.set('SumAktObsch', f"{total_sum:.2f}")
    
    # Подписант от подрядчика
    podp = SubElement(doc, 'ПодписантПодр')
    podp.set('DolzhnPodp', 'Генеральный директор')
    if act.contract and act.contract.contractor:
        podp.set('FIO', act.contract.contractor.name)
    else:
        podp.set('FIO', '________________')
    podp.set('DeystvNaOsn', 'Устава')
    
    # Главный бухгалтер
    glavbuh = SubElement(doc, 'GlavBuhgalter')
    glavbuh.set('FIO', '________________')
    
    # Преобразование в строку с кодировкой Windows-1251
    xml_str = tostring(root, encoding='windows-1251', xml_declaration=True)
    
    return xml_str
