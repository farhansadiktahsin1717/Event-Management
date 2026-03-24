from django import forms

from .models import Event


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(
            attrs={
                "class": "w-full rounded-2xl border border-slate-300 px-4 py-3 text-sm text-slate-900 shadow-sm transition focus:border-cyan-500 focus:outline-none focus:ring-2 focus:ring-cyan-200",
                "placeholder": "Your name",
            }
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "w-full rounded-2xl border border-slate-300 px-4 py-3 text-sm text-slate-900 shadow-sm transition focus:border-cyan-500 focus:outline-none focus:ring-2 focus:ring-cyan-200",
                "placeholder": "name@example.com",
            }
        ),
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "w-full rounded-2xl border border-slate-300 px-4 py-3 text-sm text-slate-900 shadow-sm transition focus:border-cyan-500 focus:outline-none focus:ring-2 focus:ring-cyan-200",
                "rows": 5,
                "placeholder": "Tell us what kind of event experience or collaboration you are looking for.",
            }
        ),
    )

    def clean_name(self):
        return (self.cleaned_data.get("name") or "").strip()

    def clean_message(self):
        message = (self.cleaned_data.get("message") or "").strip()
        if not message:
            raise forms.ValidationError("Message is required.")
        return message


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["name", "description", "date", "time", "location", "category", "image"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 px-3 py-2",
                    "placeholder": "Event name",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 px-3 py-2",
                    "rows": 4,
                    "placeholder": "Describe the event",
                }
            ),
            "date": forms.DateInput(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 px-3 py-2",
                    "type": "date",
                }
            ),
            "time": forms.TimeInput(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 px-3 py-2",
                    "type": "time",
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 px-3 py-2",
                    "placeholder": "Venue / location",
                }
            ),
            "category": forms.Select(
                attrs={"class": "w-full rounded-lg border border-slate-300 px-3 py-2"}
            ),
            "image": forms.ClearableFileInput(
                attrs={"class": "w-full rounded-lg border border-slate-300 px-3 py-2"}
            ),
        }

    def clean_name(self):
        name = (self.cleaned_data.get("name") or "").strip()
        if not name:
            raise forms.ValidationError("Event name is required.")
        return name

    def clean_location(self):
        location = (self.cleaned_data.get("location") or "").strip()
        if not location:
            raise forms.ValidationError("Location is required.")
        return location
