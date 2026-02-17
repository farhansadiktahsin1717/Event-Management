from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from categories.models import Category

from .forms import EventForm
from .models import Event


def event_list(request):
    events = Event.objects.select_related("category").prefetch_related("participants")
    categories = Category.objects.order_by("name")
    today = timezone.localdate()

    query = (request.GET.get("q") or "").strip()
    category_id = (request.GET.get("category") or "").strip()
    start_date = (request.GET.get("start_date") or "").strip()
    end_date = (request.GET.get("end_date") or "").strip()

    if query:
        events = events.filter(Q(name__icontains=query) | Q(location__icontains=query))
    if category_id:
        events = events.filter(category_id=category_id)
    if start_date:
        events = events.filter(date__gte=start_date)
    if end_date:
        events = events.filter(date__lte=end_date)

    events = events.annotate(participant_count=Count("participants", distinct=True)).order_by(
        "date", "time"
    )

    participant_totals = Event.participants.through.objects.aggregate(total=Count("id"))

    context = {
        "events": events,
        "categories": categories,
        "search_query": query,
        "selected_category": category_id,
        "start_date": start_date,
        "end_date": end_date,
        "total_participants": participant_totals["total"] or 0,
        "today": today,
    }
    return render(request, "events/event_list.html", context)


def event_detail(request, pk):
    event = get_object_or_404(
        Event.objects.select_related("category").prefetch_related("participants"),
        pk=pk,
    )
    return render(
        request,
        "events/event_detail.html",
        {
            "event": event,
            "participant_count": event.participants.count(),
        },
    )


def dashboard(request):
    events = Event.objects.select_related("category").prefetch_related("participants")
    today = timezone.localdate()

    event_counts = events.aggregate(
        total=Count("id"),
        upcoming=Count("id", filter=Q(date__gt=today)),
        past=Count("id", filter=Q(date__lt=today)),
        today=Count("id", filter=Q(date=today)),
    )
    participant_totals = Event.participants.through.objects.aggregate(total=Count("id"))
    today_events = list(events.filter(date=today).order_by("time"))
    all_events = list(events.order_by("date", "time"))
    upcoming_events = [event for event in all_events if event.date > today]
    past_events = [event for event in all_events if event.date < today]

    return render(
        request,
        "events/dashboard.html",
        {
            "counts": event_counts,
            "total_participants": participant_totals["total"] or 0,
            "today_events": today_events,
            "all_events": all_events,
            "upcoming_events": upcoming_events,
            "past_events": past_events,
            "today": today,
        },
    )


def create_event(request):
    form = EventForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Event created successfully.")
        return redirect("events:list")
    return render(request, "events/event_form.html", {"form": form, "title": "Create Event"})


def update_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        messages.success(request, "Event updated successfully.")
        return redirect("events:detail", pk=event.pk)
    return render(
        request,
        "events/event_form.html",
        {"form": form, "title": "Update Event"},
    )


def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        event.delete()
        messages.success(request, "Event deleted successfully.")
        return redirect("events:list")
    return render(request, "events/event_confirm_delete.html", {"event": event})
