from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

@login_required
def create_product(request, pk):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        product = Product.objects.create(title=title, description=description, owner=request.user)
        return redirect('product_detail', pk=product.pk)
    return render(request, 'create_product.html')

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, owner=request.user)
    if request.method == 'POST':
        product.title = request.POST['title']
        product.description = request.POST['description']
        product.save()
        return redirect('product_detail', pk=pk)
    return render(request, 'edit_product.html', {'product': product})

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, owner=request.user)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'delete_product.html', {'product': product})

@login_required
def like_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user in product.liked_by.all():
        product.liked_by.remove(request.user)
    else:
        product.liked_by.add(request.user)
    return redirect('product_list')

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})