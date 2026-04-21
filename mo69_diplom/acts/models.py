"""
Модели для приложения актов КС-2/КС-3.
ООО «Мостоотряд-69» - автоматизация сдачи-приёмки строительных работ.
"""

from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Contractor(models.Model):
    """
    Модель контрагента (подрядчик/заказчик).
    """
    name = models.CharField('Наименование организации', max_length=255)
    inn = models.CharField('ИНН', max_length=12, unique=True)
    kpp = models.CharField('КПП', max_length=9, blank=True)
    ogrn = models.CharField('ОГРН', max_length=13, blank=True)
    legal_address = models.TextField('Юридический адрес', blank=True)
    actual_address = models.TextField('Фактический адрес', blank=True)
    phone = models.CharField('Телефон', max_length=50, blank=True)
    email = models.EmailField('Email', blank=True)
    director_name = models.CharField('ФИО директора', max_length=255, blank=True)
    director_position = models.CharField('Должность директора', max_length=255, default='Генеральный директор')
    bank_name = models.CharField('Наименование банка', max_length=255, blank=True)
    bik = models.CharField('БИК', max_length=9, blank=True)
    correspondent_account = models.CharField('Корр. счет', max_length=20, blank=True)
    checking_account = models.CharField('Расчетный счет', max_length=20, blank=True)
    
    class Meta:
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагенты'
        ordering = ['name']
    
    def __str__(self):
        return f'{self.name} (ИНН {self.inn})'


class Object(models.Model):
    """
    Модель объекта строительства.
    """
    name = models.CharField('Наименование объекта', max_length=255)
    code = models.CharField('Код объекта', max_length=50, blank=True)
    address = models.TextField('Адрес объекта', blank=True)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Объект строительства'
        verbose_name_plural = 'Объекты строительства'
        ordering = ['name']
    
    def __str__(self):
        return f'{self.name}'


class WorkType(models.Model):
    """
    Модель вида работ (справочник).
    """
    name = models.CharField('Наименование вида работ', max_length=255)
    code = models.CharField('Код вида работ', max_length=50, blank=True)
    unit = models.CharField('Единица измерения', max_length=50, default='м3')
    description = models.TextField('Описание', blank=True)
    
    class Meta:
        verbose_name = 'Вид работ'
        verbose_name_plural = 'Виды работ'
        ordering = ['name']
    
    def __str__(self):
        return f'{self.name} ({self.unit})'


class Contract(models.Model):
    """
    Модель договора подряда.
    """
    number = models.CharField('Номер договора', max_length=50)
    date = models.DateField('Дата договора')
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, related_name='contracts', verbose_name='Контрагент')
    object = models.ForeignKey(Object, on_delete=models.CASCADE, related_name='contracts', verbose_name='Объект')
    amount = models.DecimalField('Сумма договора', max_digits=15, decimal_places=2, default=0)
    start_date = models.DateField('Дата начала работ', null=True, blank=True)
    end_date = models.DateField('Дата окончания работ', null=True, blank=True)
    description = models.TextField('Описание договора', blank=True)
    file = models.FileField('Файл договора', upload_to='contracts/', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Договор'
        verbose_name_plural = 'Договоры'
        ordering = ['-date']
        unique_together = ['number', 'contractor']
    
    def __str__(self):
        return f'Договор №{self.number} от {self.date.strftime("%d.%m.%Y")} - {self.contractor.name}'
    
    def total_sum(self):
        """Возвращает общую сумму по всем актам в рамках договора."""
        total = Act.objects.filter(contract=self, is_deleted=False).aggregate(
            total=models.Sum('total_amount')
        )['total']
        return total if total else Decimal('0.00')


class Act(models.Model):
    """
    Модель акта КС-2 (акт о приёмке выполненных работ).
    """
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('review', 'На согласовании'),
        ('approved', 'Подписан'),
        ('paid', 'Оплачен'),
        ('rejected', 'Отклонён'),
    ]
    
    number = models.CharField('Номер акта', max_length=50)
    date = models.DateField('Дата акта')
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='acts', verbose_name='Договор')
    object = models.ForeignKey(Object, on_delete=models.CASCADE, related_name='acts', verbose_name='Объект')
    period_start = models.DateField('Период с', null=True, blank=True)
    period_end = models.DateField('Период по', null=True, blank=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='draft')
    total_amount = models.DecimalField('Итоговая сумма', max_digits=15, decimal_places=2, default=0)
    nds_amount = models.DecimalField('В том числе НДС', max_digits=15, decimal_places=2, default=0)
    nds_rate = models.DecimalField('Ставка НДС (%)', max_digits=5, decimal_places=2, default=20)
    without_nds = models.BooleanField('Без НДС', default=False)
    notes = models.TextField('Примечание', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Создал')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    is_deleted = models.BooleanField('Удалён', default=False)
    
    class Meta:
        verbose_name = 'Акт КС-2'
        verbose_name_plural = 'Акты КС-2'
        ordering = ['-date', '-number']
        unique_together = ['number', 'contract']
    
    def __str__(self):
        return f'Акт №{self.number} от {self.date.strftime("%d.%m.%Y")} - {self.contract.contractor.name}'
    
    def total_sum(self):
        """Возвращает общую сумму по всем строкам акта."""
        return self.total_amount
    
    def calculate_totals(self):
        """Пересчитывает итоговые суммы по строкам акта."""
        items = self.items.filter(is_deleted=False)
        subtotal = sum(item.total for item in items)
        
        if self.without_nds:
            self.total_amount = subtotal
            self.nds_amount = Decimal('0.00')
        else:
            # Сумма включает НДС
            self.nds_amount = subtotal * self.nds_rate / (100 + self.nds_rate)
            self.total_amount = subtotal
        
        self.save()
        return self.total_amount


class ActItem(models.Model):
    """
    Строка акта КС-2 (выполненная работа).
    """
    act = models.ForeignKey(Act, on_delete=models.CASCADE, related_name='items', verbose_name='Акт')
    work_type = models.ForeignKey(WorkType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Вид работ')
    number = models.PositiveIntegerField('№ п/п', default=1)
    name = models.CharField('Наименование работ', max_length=500)
    unit = models.CharField('Ед. изм.', max_length=50, default='м3')
    quantity = models.DecimalField('Количество', max_digits=15, decimal_places=4, default=0)
    price = models.DecimalField('Цена за ед.', max_digits=15, decimal_places=2, default=0)
    total = models.DecimalField('Стоимость', max_digits=15, decimal_places=2, default=0)
    notes = models.TextField('Примечание', blank=True)
    is_deleted = models.BooleanField('Удалена', default=False)
    
    class Meta:
        verbose_name = 'Строка акта'
        verbose_name_plural = 'Строки актов'
        ordering = ['number']
    
    def __str__(self):
        return f'{self.number}. {self.name}'
    
    def save(self, *args, **kwargs):
        """Автоматически рассчитывает стоимость при сохранении."""
        self.total = self.quantity * self.price
        super().save(*args, **kwargs)
    
    def total_sum(self):
        """Возвращает стоимость строки."""
        return self.total
