from django import forms

import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check if a date is not in the past
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        return data


class BorrowBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 2 weeks (default 1 week).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check if a date is not in the past
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today)
        if data > datetime.date.today() + datetime.timedelta(weeks=2):
            raise ValidationError(_('Invalid date - renewal more than 2 weeks ahead'))

        return data


class BackBookForm(forms.Form):
    Back_book = forms.BooleanField(help_text="Is the book already on the library shelf?")

    def clean_renewal_date(self):
        if not self.Back_book:
            raise ValidationError("put book on library shelf")
        return self.Back_book