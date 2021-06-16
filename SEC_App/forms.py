from django.db.models import fields
from SEC_App.models import Request
from django import forms
from datetime import date

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['keyword', 'period_start', 'period_end', 'time_start', 'time_end', 'rangeOfsearch', 'includeAll']