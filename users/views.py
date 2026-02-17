from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ParticipantForm
from .models import Participant


def participant_list(request):
    participants = Participant.objects.prefetch_related("events").order_by("name")
    return render(
        request,
        "users/participant_list.html",
        {"participants": participants},
    )


def create_participant(request):
    form = ParticipantForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Participant created successfully.")
        return redirect("users:list")
    return render(
        request,
        "users/participant_form.html",
        {"form": form, "title": "Create Participant"},
    )


def update_participant(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    form = ParticipantForm(request.POST or None, instance=participant)
    if form.is_valid():
        form.save()
        messages.success(request, "Participant updated successfully.")
        return redirect("users:list")
    return render(
        request,
        "users/participant_form.html",
        {"form": form, "title": "Update Participant"},
    )


def delete_participant(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == "POST":
        participant.delete()
        messages.success(request, "Participant deleted successfully.")
        return redirect("users:list")
    return render(
        request,
        "users/participant_confirm_delete.html",
        {"participant": participant},
    )
