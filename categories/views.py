from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from users.utils import role_flags_for_user, role_required

from .forms import CategoryForm
from .models import Category


def with_role_context(request, context=None):
    base = role_flags_for_user(request.user)
    if context:
        base.update(context)
    return base


@role_required("Admin", "Organizer")
def category_list(request):
    categories = Category.objects.order_by("name")
    return render(request, "categories/category_list.html", with_role_context(request, {"categories": categories}))


@role_required("Admin", "Organizer")
def create_category(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Category created successfully.")
        return redirect("categories:list")
    return render(
        request,
        "categories/category_form.html",
        with_role_context(request, {"form": form, "title": "Create Category"}),
    )


@role_required("Admin", "Organizer")
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
        with_role_context(request, {"form": form, "title": "Update Category"}),
    )


@role_required("Admin", "Organizer")
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted successfully.")
        return redirect("categories:list")
    return render(
        request,
        "categories/category_confirm_delete.html",
        with_role_context(request, {"category": category}),
    )
