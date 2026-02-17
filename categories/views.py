from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoryForm
from .models import Category


def category_list(request):
    categories = Category.objects.order_by("name")
    return render(request, "categories/category_list.html", {"categories": categories})


def create_category(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Category created successfully.")
        return redirect("categories:list")
    return render(
        request,
        "categories/category_form.html",
        {"form": form, "title": "Create Category"},
    )


def update_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        messages.success(request, "Category updated successfully.")
        return redirect("categories:list")
    return render(
        request,
        "categories/category_form.html",
        {"form": form, "title": "Update Category"},
    )


def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted successfully.")
        return redirect("categories:list")
    return render(
        request,
        "categories/category_confirm_delete.html",
        {"category": category},
    )
