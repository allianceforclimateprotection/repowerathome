from django.contrib.admin import widgets

from rah.models import Profile
from commitments.models import Contributor
from events.models import Guest

from django import forms

class UserExportForm(forms.Form):
    date_filter_start = forms.DateField(required=False, label="Filter activity before",
        widget=widgets.AdminDateWidget())
    date_filter_end = forms.DateField(required=False, label="Filter activity after",
        widget=widgets.AdminDateWidget())
    filter_inactive = forms.BooleanField(required=False, label="Filter users with no activity")
    include_guests = forms.BooleanField(required=False, label="Include contributors who have entered commitments")
    excel_friendly = forms.BooleanField(required=False)

    def save_to_writer(self, writer):
        date_start = self.cleaned_data["date_filter_start"] if "date_filter_start" in self.cleaned_data else None
        date_end = self.cleaned_data["date_filter_end"] if "date_filter_end" in self.cleaned_data else None
        queryset = Profile.objects.user_engagement(date_start=date_start, date_end=date_end)
        if self.cleaned_data["include_guests"]:
            guest_queryset = Contributor.objects.contirbutor_engagment(date_start=date_start, date_end=date_end)
            queryset = queryset + guest_queryset[1:]
        for row in queryset:
            if not self.cleaned_data["filter_inactive"] or any(row[8:]):
                writer.writerow(['="%s"' % s if s and self.cleaned_data["excel_friendly"] else s for s in row])
