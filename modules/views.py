from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import GangSheet, GangSheetItem, Module
from .forms import GangSheetForm, GangSheetItemForm, ModuleForm
from products.models import CustomizedProduct

@login_required
def module_list(request):
    modules = Module.objects.filter(user=request.user)
    return render(request, 'modules/list.html', {
        'modules': modules,
        'active_menu': 'modules'
    })

@login_required
def create_module(request):
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.user = request.user
            module.save()
            messages.success(request, 'Module created successfully!')
            return redirect('modules:list')
    else:
        form = ModuleForm()
    
    return render(request, 'modules/create.html', {
        'form': form,
        'active_menu': 'modules'
    })

@login_required
def gangsheet_builder(request):
    gangsheets = GangSheet.objects.filter(user=request.user)
    products = CustomizedProduct.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = GangSheetForm(request.POST)
        if form.is_valid():
            gangsheet = form.save(commit=False)
            gangsheet.user = request.user
            gangsheet.save()
            messages.success(request, 'GangSheet created successfully!')
            return redirect('modules:gangsheet_detail', gangsheet_id=gangsheet.id)
    else:
        form = GangSheetForm()
    
    return render(request, 'modules/gangsheet_builder.html', {
        'gangsheets': gangsheets,
        'products': products,
        'form': form,
        'active_menu': 'gangsheet'
    })

@login_required
def gangsheet_detail(request, gangsheet_id):
    gangsheet = get_object_or_404(GangSheet, id=gangsheet_id, user=request.user)
    items = GangSheetItem.objects.filter(gangsheet=gangsheet)
    
    if request.method == 'POST':
        form = GangSheetItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.gangsheet = gangsheet
            item.save()
            messages.success(request, 'Item added to GangSheet successfully!')
            return redirect('modules:gangsheet_detail', gangsheet_id=gangsheet.id)
    else:
        form = GangSheetItemForm()
        form.fields['product'].queryset = CustomizedProduct.objects.filter(user=request.user)
    
    return render(request, 'modules/gangsheet_detail.html', {
        'gangsheet': gangsheet,
        'items': items,
        'form': form,
        'active_menu': 'gangsheet'
    })