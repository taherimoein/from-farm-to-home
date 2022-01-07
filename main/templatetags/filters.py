from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.dateparse import parse_date, parse_datetime
from django.shortcuts import reverse
from datetime import datetime, date
from django.utils import timezone
from main.models import User
from django import template
import jdatetime

register = template.Library()

# -------------------------------------------------------------------------------------------------------------------------------------

def currency(value):
    return '{:,}'.format(int(value))
register.filter('currency', currency)


def gregorian_to_jalali_date(value):
    date_format = "%Y-%m-%d"
    thisdate = datetime.strptime(str(value), date_format)
    return jdatetime.date.fromgregorian(day = thisdate.day, month = thisdate.month, year = thisdate.year).strftime("%Y/%m/%d")
register.filter('date_to_jalali', gregorian_to_jalali_date)

def gregorian_to_jalali_datetime(value):
    date_format = "%Y-%m-%d"
    thisdate = datetime.strptime(str(value.date()), date_format)
    return jdatetime.date.fromgregorian(day = thisdate.day, month = thisdate.month, year = thisdate.year).strftime("%Y/%m/%d")
register.filter('datetime_to_jalali', gregorian_to_jalali_datetime)
