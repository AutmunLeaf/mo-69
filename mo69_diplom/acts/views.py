"""
Представления (views) для приложения актов КС-2/КС-3.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum, Count, Q
from django.template.loader import render_to_string
from django.utils import timezone
from decimal import Decimal
import json

from .models import Contractor, Object, WorkType, Contract, Act, ActItem
from .forms import (
    ActForm, ActItemForm, ActItemFormSet,
    ContractorForm, ObjectForm, ContractForm, WorkTypeForm
)
from .xml_generator import generate_ks2_xml, generate_ks3_xml
from .validators import validate_xml


@login_required
def dashboard(request):
    """
    Главная страница - дашборд со статистикой и списком актов.
    """
    # Статистика
    total_acts = Act.objects.filter(is_deleted=False).count()
    draft_acts = Act.objects.filter(status='draft', is_deleted=False).count()
    review_acts = Act.objects.filter(status='review', is_deleted=False).count()
    approved_acts = Act.objects.filter(status='approved', is_deleted=False).count()
    paid_acts = Act.objects.filter(status='paid', is_deleted=False).count()
    
    total_amount = Act.objects.filter(is_deleted=False).aggregate(
        total=Sum('total_amount')
    )['total'] or Decimal('0.00')
    
    # Последние акты
    recent_acts = Act.objects.filter(is_deleted=False).select_related(
        'contract', 'contract__contractor', 'object'
    )[:10]
    
    context = {
        'total_acts': total_acts,
        'draft_acts': draft_acts,
        'review_acts': review_acts,
        'approved_acts': approved_acts,
        'paid_acts': paid_acts,
        'total_amount': total_amount,
        'recent_acts': recent_acts,
    }
    return render(request, 'acts/dashboard.html', context)


@login_required
def create_act(request):
    """
    Создание нового акта КС-2.
    """
    if request.method == 'POST':
        act_form = ActForm(request.POST)
        item_formset = ActItemFormSet(request.POST, prefix='items')
        
        if act_form.is_valid() and item_formset.is_valid():
            act = act_form.save(commit=False)
            act.created_by = request.user
            act.save()
            
            items = item_formset.save(commit=False)
            for i, item in enumerate(items, 1):
                item.act = act
                item.number = i
                item.save()
            
            # Пересчитываем итоги
            act.calculate_totals()
            
            return redirect('act_detail', pk=act.pk)
    else:
        act_form = ActForm()
        item_formset = ActItemFormSet(prefix='items')
    
    context = {
        'act_form': act_form,
        'item_formset': item_formset,
    }
    return render(request, 'acts/create_act.html', context)


@login_required
def act_detail(request, pk):
    """
    Просмотр деталей акта.
    """
    act = get_object_or_404(Act.objects.select_related(
        'contract', 'contract__contractor', 'object', 'created_by'
    ), pk=pk)
    items = act.items.filter(is_deleted=False)
    
    context = {
        'act': act,
        'items': items,
    }
    return render(request, 'acts/act_detail.html', context)


@login_required
def generate_ks2_pdf(request, pk):
    """
    Генерация PDF формы КС-2.
    """
    act = get_object_or_404(Act, pk=pk)
    items = act.items.filter(is_deleted=False)
    
    html = render_to_string('acts/ks2_template.html', {
        'act': act,
        'items': items,
        'contractor': act.contract.contractor,
        'object': act.object,
    })
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="KS-2_{act.number}.pdf"'
    response.write(html.encode('utf-8'))
    return response


@login_required
def generate_ks3_pdf(request, pk):
    """
    Генерация PDF формы КС-3.
    """
    act = get_object_or_404(Act, pk=pk)
    items = act.items.filter(is_deleted=False)
    
    html = render_to_string('acts/ks3_template.html', {
        'act': act,
        'items': items,
        'contractor': act.contract.contractor,
        'object': act.object,
    })
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="KS-3_{act.number}.pdf"'
    response.write(html.encode('utf-8'))
    return response


@login_required
def generate_ks2_xml_file(request, pk):
    """
    Генерация XML файла КС-2 по формату Приказа ФНС № ЕД-7-26/691.
    """
    act = get_object_or_404(Act, pk=pk)
    items = act.items.filter(is_deleted=False)
    
    xml_content = generate_ks2_xml(act, items)
    
    response = HttpResponse(xml_content, content_type='application/xml')
    response['Content-Disposition'] = f'attachment; filename="KS-2_{act.number}.xml"'
    response.charset = 'windows-1251'
    return response


@login_required
def generate_ks3_xml_file(request, pk):
    """
    Генерация XML файла КС-3.
    """
    act = get_object_or_404(Act, pk=pk)
    items = act.items.filter(is_deleted=False)
    
    xml_content = generate_ks3_xml(act, items)
    
    response = HttpResponse(xml_content, content_type='application/xml')
    response['Content-Disposition'] = f'attachment; filename="KS-3_{act.number}.xml"'
    response.charset = 'windows-1251'
    return response


@login_required
def validate_xml_page(request):
    """
    Страница проверки валидности XML файла.
    """
    result = None
    if request.method == 'POST' and request.FILES.get('xml_file'):
        xml_file = request.FILES['xml_file']
        xml_content = xml_file.read().decode('utf-8')
        result = validate_xml(xml_content)
    
    context = {'result': result}
    return render(request, 'acts/validate_xml.html', context)


@login_required
def contractors_list(request):
    """
    Список контрагентов.
    """
    contractors = Contractor.objects.all()
    context = {'contractors': contractors}
    return render(request, 'acts/contractors_list.html', context)


@login_required
def objects_list(request):
    """
    Список объектов строительства.
    """
    objects = Object.objects.all()
    context = {'objects': objects}
    return render(request, 'acts/objects_list.html', context)


@login_required
def contracts_list(request):
    """
    Список договоров.
    """
    contracts = Contract.objects.select_related('contractor', 'object').all()
    context = {'contracts': contracts}
    return render(request, 'acts/contracts_list.html', context)


@login_required
def work_types_list(request):
    """
    Список видов работ.
    """
    work_types = WorkType.objects.all()
    context = {'work_types': work_types}
    return render(request, 'acts/work_types_list.html', context)
