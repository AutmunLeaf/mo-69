"""
Генератор XML файлов для форм КС-2 и КС-3
Соответствует Приказу ФНС России № ЕД-7-26/691
"""

import uuid
from datetime import datetime
from lxml import etree


def generate_ks2_xml(act, items):
    """
    Генерация XML для КС-2 по Приказу ФНС № ЕД-7-26/691
    
    Args:
        act: объект модели Act
        items: queryset объектов ActItem
    
    Returns:
        bytes: XML контент в кодировке Windows-1251
    """
    # Создаем корневой элемент
    root = etree.Element(
        "Файл",
        xmlns="http://www.nalog.ru/edocs/ks2",
        ИдФайл=f"KS2-{uuid.uuid4().hex[:10].upper()}",
        ВерсПрог="5.2",
        ВерсФорм="5.0"
    )
    
    # Создаем элемент Документ
    document = etree.SubElement(root, "Документ")
    
    # Код вида документа (КС-2)
    knd = etree.SubElement(document, "КНД")
    knd.text = "1110335"
    
    # Дата и время формирования
    date_info = etree.SubElement(document, "ДатаИнфПодр")
    date_info.text = act.created_at.strftime("%d.%m.%Y")
    
    time_info = etree.SubElement(document, "ВремИнфПодр")
    time_info.text = act.created_at.strftime("%H:%M:%S")
    
    # Наименование экономического субъекта-составителя
    org_name = etree.SubElement(document, "НаимЭкСубСост")
    org_name.text = "ООО «Мостоотряд-69»"
    
    # Сведения об акте сдачи-приемки
    sv_act = etree.SubElement(document, "СвАктСдПр")
    
    # Номер акта
    nom_act = etree.SubElement(sv_act, "НомАкт")
    nom_act.text = str(act.number)
    
    # Дата акта
    data_act = etree.SubElement(sv_act, "ДатаАкт")
    data_act.text = act.created_at.strftime("%d.%m.%Y")
    
    # Объект строительства
    object_name = etree.SubElement(sv_act, "НаимОбъект")
    object_name.text = act.object.name
    
    # Договор
    dogovor = etree.SubElement(sv_act, "СвДоговор")
    nom_dog = etree.SubElement(dogovor, "НомДоговор")
    nom_dog.text = act.contract.number
    data_dog = etree.SubElement(dogovor, "ДатаДоговор")
    data_dog.text = act.contract.date.strftime("%d.%m.%Y") if act.contract.date else ""
    
    # Период выполнения работ
    period = etree.SubElement(sv_act, "ПериодВыполн")
    data_nach = etree.SubElement(period, "ДатаНач")
    data_nach.text = act.period_start.strftime("%d.%m.%Y") if act.period_start else ""
    data_okon = etree.SubElement(period, "ДатаОкон")
    data_okon.text = act.period_end.strftime("%d.%m.%Y") if act.period_end else ""
    
    # Заказчик
    zakazchik = etree.SubElement(sv_act, "Заказчик")
    naam_zak = etree.SubElement(zakazchik, "НаимОрг")
    naam_zak.text = act.contract.contractor.name
    inn_zak = etree.SubElement(zakazchik, "ИНН")
    inn_zak.text = act.contract.contractor.inn or ""
    
    # Элементы работ (цикл по items)
    for idx, item in enumerate(items, 1):
        naim_ist = etree.SubElement(document, "НаимИСт")
        
        # Номер позиции
        nom_poz = etree.SubElement(naim_ist, "НомПоз")
        nom_poz.text = str(idx)
        
        # Номер позиции по смете
        nom_smet = etree.SubElement(naim_ist, "НомПозСмет")
        nom_smet.text = item.work_code or ""
        
        # Наименование работы
        naam_rab = etree.SubElement(naim_ist, "НаимРабот")
        naam_rab.text = item.work_type.name
        
        # Номер единичной расценки
        nom_ras = etree.SubElement(naim_ist, "НомРасц")
        nom_ras.text = item.unit_rate or ""
        
        # Единица измерения
        ed_izm = etree.SubElement(naim_ist, "ЕдИзм")
        ed_izm.text = item.unit or ""
        
        # Количество
        kol_vo = etree.SubElement(naim_ist, "КолВо")
        kol_vo.text = str(item.quantity)
        
        # Цена за единицу
        cena_ed = etree.SubElement(naim_ist, "ЦенаЕд")
        cena_ed.text = f"{item.unit_price:.2f}"
        
        # Стоимость
        stoim = etree.SubElement(naim_ist, "Стоимость")
        stoim.text = f"{item.total:.2f}"
    
    # Настройки формирования документа
    nastr_form = etree.SubElement(document, "НастрФормДок")
    priznak_print = etree.SubElement(nastr_form, "ПризнакПечать")
    priznak_print.text = "Бумажный документ"
    
    # Итоговые суммы
    vsego_akt = etree.SubElement(document, "ВсегоАктОтч")
    summa_vsego = etree.SubElement(vsego_akt, "СуммаВсего")
    summa_vsego.text = f"{act.total_sum:.2f}"
    
    # Подписант от подрядчика
    podpisan = etree.SubElement(document, "ПодписантПодр")
    dolzhn = etree.SubElement(podpisan, "Должн")
    dolzhn.text = "Руководитель организации"
    fio_podp = etree.SubElement(podpisan, "ФИОПодп")
    fio_podp.text = "Генеральный директор"
    
    # Сериализация в строку с кодировкой Windows-1251
    xml_str = etree.tostring(
        root,
        pretty_print=True,
        encoding='windows-1251',
        xml_declaration=True
    )
    
    return xml_str


def generate_ks3_xml(act, items):
    """
    Генерация XML для КС-3 по Приказу ФНС № ЕД-7-26/691
    
    Args:
        act: объект модели Act
        items: queryset объектов ActItem
    
    Returns:
        bytes: XML контент в кодировке Windows-1251
    """
    # Создаем корневой элемент
    root = etree.Element(
        "Файл",
        xmlns="http://www.nalog.ru/edocs/ks3",
        ИдФайл=f"KS3-{uuid.uuid4().hex[:10].upper()}",
        ВерсПрог="5.2",
        ВерсФорм="5.0"
    )
    
    # Создаем элемент Документ
    document = etree.SubElement(root, "Документ")
    
    # Код вида документа (КС-3)
    knd = etree.SubElement(document, "КНД")
    knd.text = "1110336"
    
    # Дата и время формирования
    date_info = etree.SubElement(document, "ДатаИнфПодр")
    date_info.text = act.created_at.strftime("%d.%m.%Y")
    
    time_info = etree.SubElement(document, "ВремИнфПодр")
    time_info.text = act.created_at.strftime("%H:%M:%S")
    
    # Наименование экономического субъекта-составителя
    org_name = etree.SubElement(document, "НаимЭкСубСост")
    org_name.text = "ООО «Мостоотряд-69»"
    
    # Сведения о справке
    sv_spravka = etree.SubElement(document, "СвСправка")
    
    # Номер справки
    nom_spravka = etree.SubElement(sv_spravka, "НомСправка")
    nom_spravka.text = str(act.number)
    
    # Дата справки
    data_spravka = etree.SubElement(sv_spravka, "ДатаСправка")
    data_spravka.text = act.created_at.strftime("%d.%m.%Y")
    
    # Объект строительства
    object_name = etree.SubElement(sv_spravka, "НаимОбъект")
    object_name.text = act.object.name
    
    # Договор
    dogovor = etree.SubElement(sv_spravka, "СвДоговор")
    nom_dog = etree.SubElement(dogovor, "НомДоговор")
    nom_dog.text = act.contract.number
    data_dog = etree.SubElement(dogovor, "ДатаДоговор")
    data_dog.text = act.contract.date.strftime("%d.%m.%Y") if act.contract.date else ""
    
    # Период выполнения работ
    period = etree.SubElement(sv_spravka, "ПериодВыполн")
    data_nach = etree.SubElement(period, "ДатаНач")
    data_nach.text = act.period_start.strftime("%d.%m.%Y") if act.period_start else ""
    data_okon = etree.SubElement(period, "ДатаОкон")
    data_okon.text = act.period_end.strftime("%d.%m.%Y") if act.period_end else ""
    
    # Заказчик
    zakazchik = etree.SubElement(sv_spravka, "Заказчик")
    naam_zak = etree.SubElement(zakazchik, "НаимОрг")
    naam_zak.text = act.contract.contractor.name
    inn_zak = etree.SubElement(zakazchik, "ИНН")
    inn_zak.text = act.contract.contractor.inn or ""
    
    # Элементы работ (цикл по items)
    for idx, item in enumerate(items, 1):
        naim_ist = etree.SubElement(document, "НаимИСт")
        
        # Номер позиции
        nom_poz = etree.SubElement(naim_ist, "НомПоз")
        nom_poz.text = str(idx)
        
        # Наименование работы
        naam_rab = etree.SubElement(naim_ist, "НаимРабот")
        naam_rab.text = item.work_type.name
        
        # Единица измерения
        ed_izm = etree.SubElement(naim_ist, "ЕдИзм")
        ed_izm.text = item.unit or ""
        
        # Стоимость
        stoim = etree.SubElement(naim_ist, "Стоимость")
        stoim.text = f"{item.total:.2f}"
    
    # Настройки формирования документа
    nastr_form = etree.SubElement(document, "НастрФормДок")
    priznak_print = etree.SubElement(nastr_form, "ПризнакПечать")
    priznak_print.text = "Бумажный документ"
    
    # Итоговые суммы
    vsego_spravka = etree.SubElement(document, "ВсегоСправкаОтч")
    summa_vsego = etree.SubElement(vsego_spravka, "СуммаВсего")
    summa_vsego.text = f"{act.total_sum:.2f}"
    
    # Подписант от подрядчика
    podpisan = etree.SubElement(document, "ПодписантПодр")
    dolzhn = etree.SubElement(podpisan, "Должн")
    dolzhn.text = "Руководитель организации"
    fio_podp = etree.SubElement(podpisan, "ФИОПодп")
    fio_podp.text = "Генеральный директор"
    
    # Главный бухгалтер
    glavbuх = etree.SubElement(document, "ГлавБух")
    fio_gb = etree.SubElement(glavbuх, "ФИО")
    fio_gb.text = ""
    
    # Сериализация в строку с кодировкой Windows-1251
    xml_str = etree.tostring(
        root,
        pretty_print=True,
        encoding='windows-1251',
        xml_declaration=True
    )
    
    return xml_str
