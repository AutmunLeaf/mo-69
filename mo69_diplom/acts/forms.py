"""
Формы для приложения актов КС-2/КС-3.
"""

from django import forms
from django.forms import inlineformset_factory
from .models import Contractor, Object, WorkType, Contract, Act, ActItem


class ContractorForm(forms.ModelForm):
    """Форма для создания/редактирования контрагента."""
    
    class Meta:
        model = Contractor
        fields = [
            'name', 'inn', 'kpp', 'ogrn', 'legal_address', 'actual_address',
            'phone', 'email', 'director_name', 'director_position',
            'bank_name', 'bik', 'correspondent_account', 'checking_account'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'inn': forms.TextInput(attrs={'class': 'form-control'}),
            'kpp': forms.TextInput(attrs={'class': 'form-control'}),
            'ogrn': forms.TextInput(attrs={'class': 'form-control'}),
            'legal_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'actual_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'director_name': forms.TextInput(attrs={'class': 'form-control'}),
            'director_position': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bik': forms.TextInput(attrs={'class': 'form-control'}),
            'correspondent_account': forms.TextInput(attrs={'class': 'form-control'}),
            'checking_account': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ObjectForm(forms.ModelForm):
    """Форма для создания/редактирования объекта строительства."""
    
    class Meta:
        model = Object
        fields = ['name', 'code', 'address', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class WorkTypeForm(forms.ModelForm):
    """Форма для создания/редактирования вида работ."""
    
    class Meta:
        model = WorkType
        fields = ['name', 'code', 'unit', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class ContractForm(forms.ModelForm):
    """Форма для создания/редактирования договора."""
    
    class Meta:
        model = Contract
        fields = ['number', 'date', 'contractor', 'object', 'amount', 
                  'start_date', 'end_date', 'description', 'file']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'contractor': forms.Select(attrs={'class': 'form-control'}),
            'object': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ActItemForm(forms.ModelForm):
    """Форма для строки акта."""
    
    class Meta:
        model = ActItem
        fields = ['work_type', 'number', 'name', 'unit', 'quantity', 'price', 'notes']
        widgets = {
            'work_type': forms.Select(attrs={'class': 'form-control work-type-select'}),
            'number': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'name': forms.TextInput(attrs={'class': 'form-control work-name'}),
            'unit': forms.TextInput(attrs={'class': 'form-control work-unit'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control work-quantity', 'step': '0.0001'}),
            'price': forms.NumberInput(attrs={'class': 'form-control work-price', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
        }


class ActForm(forms.ModelForm):
    """Форма для создания/редактирования акта КС-2."""
    
    class Meta:
        model = Act
        fields = ['number', 'date', 'contract', 'object', 'period_start', 'period_end',
                  'status', 'nds_rate', 'without_nds', 'notes']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'contract': forms.Select(attrs={'class': 'form-control'}),
            'object': forms.Select(attrs={'class': 'form-control'}),
            'period_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'period_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'nds_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'without_nds': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# Inline форма для строк акта
ActItemFormSet = inlineformset_factory(
    Act,
    ActItem,
    form=ActItemForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
)
