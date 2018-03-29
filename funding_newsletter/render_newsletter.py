import sys, os
from django.utils.dateparse import parse_datetime
from funding_opportunities_models.models import FundingOpportunity
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import models
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.timezone import is_aware, make_aware
from datetime import timedelta
from dateutil.relativedelta import relativedelta


NEW_FUNDS_N_DAYS = 5*30  # show new funding opportunities with
NEW_FUNDS_N_MAX = 6  # Maximum of funds to send
CLOSING_FUNDS_N_DAYS = 30  # number of days required for a fund to be considered a closing fund.
ROLLING_FUNDS_MONTHS = [3, 6, 9]


def today():
    """Returns localized today datetime object"""
    return timezone.localtime().replace(
        hour=0, minute=0, second=0, microsecond=0)


def next_monday(skip=0):
    """Returns next monday as a datetime object.

    Newsletter dissemination is done every monday.
    This is useful to simulate the newsletter in the future.
    `skip` is the number of weeks to move further.
    """

    day = today()
    weekday = day.weekday()

    dt = timedelta(days=((skip*7)-weekday))

    if weekday == 0:  # is monday
        return day + dt if skip else day
    else:
        return day + dt + timedelta(days=7)


# def todayaware_datetime(date_str):
#     ret = parse_datetime(date_str)
#     if not is_aware(ret):
#         ret = make_aware(ret)
#     return ret


# def find_first_monday(year, month):
#     d = date(year, 1, 4)  # The Jan 4th must be in week 1  according to ISO
#     d = d + relativedelta(months=+month-1)
#     d = d + timedelta(days=-d.weekday())
#     if (d.month < month):
#         d = d + timedelta(days=7)
#     return d


def query_new(start_date=None):
    """New funding opportunities that have not been disseminated"""

    # day = today()
    # next_tuesday = day if day.weekday() == 0 else next_monday(skip)

    start_date = start_date or next_monday()
    limit_date = start_date + timedelta(days=NEW_FUNDS_N_DAYS)

    newfunds = FundingOpportunity.objects.filter(
        fundingopportunity_end__gt=start_date,
        fundingopportunity_end__lt=limit_date,
        fundingopportunity_published=False,
        fundingopportunity_end__isnull=False,
    ).order_by(
        'fundingopportunity_end',
        'fundingopportunity_name',
    )[:NEW_FUNDS_N_MAX]
    newfunds = sorted(
        newfunds, key=lambda x: x.subject.opportunitysubject_order)

    return newfunds


def query_closing(start_date=None):
    """ Closing in 30 days"""

    start_date = start_date or next_monday()
    limit_date = start_date + timedelta(days=CLOSING_FUNDS_N_DAYS)

    closingfunds = FundingOpportunity.objects.filter(
        fundingopportunity_end__gt=start_date,
        fundingopportunity_end__lt=limit_date,
        fundingopportunity_end__isnull=False,
    ).order_by(
        'fundingopportunity_end',
        'fundingopportunity_name',
    )
    closingfunds = sorted(
        closingfunds, key=lambda x: x.subject.opportunitysubject_order)

    return closingfunds


# def query_rolling(skip=1):
#     """ Rolling Opportunities
#     They should be generated only on the first monday of
#     May, September and January
#     """
#     month = next_monday(skip).month

#     if month in ROLLING_FUNDS_MONTHS:
#         first_monday = find_first_monday(next_monday(skip).year, month)
#         previous_tuesday = first_monday + timedelta(days=-6)

#         if previous_tuesday <= next_monday(skip).date() <= first_monday:
#             rollingfunds = FundingOpportunity.objects.all()
#             rollingfunds = rollingfunds.filter(fundingopportunity_end=None)
#             rollingfunds = rollingfunds.order_by(
#                 'fundingopportunity_end', 'fundingopportunity_name')
#             rollingfunds = sorted(
#                 rollingfunds, key=lambda x: x.subject.opportunitysubject_order)
#         else:
#             rollingfunds = []
#     else:
#         rollingfunds = []

#     return rollingfunds


def render_newsletter(skip=0):

    # Collect opportunities that were disseminated, allegedly...
    skipped_opportunities = []
    # print(start_date.date())
    for i in range(0, skip):
        start_date = next_monday(i)
        print(start_date.date())
        newfunds = query_new(start_date)

        # and mark them as published
        for o in newfunds:
            print(start_date, "FAKE Publishing", o)
            o.fundingopportunity_published = True
            o.save()

        skipped_opportunities.extend(newfunds)

    # generate the newsletter
    start_date = next_monday(skip)
    newfunds = query_new(start_date)
    closingfunds = query_closing(start_date)
    rollingfunds = []  # query_rolling(skip) FIXME !!!!!!!!!!!!!!!!!!!!!

    if newfunds:
        body = render_to_string(
            'funding_newsletter/funding-opportunities-newsletter.html',
            {
                'newfunds':     newfunds,
                'closingfunds': closingfunds,
                'rollingfunds': rollingfunds,
            }
        )
    else:
        body = (
            '<div align="center">'
            '<p class="ui blue">Funding opportunities disseminated for this week</p>'
            '<i class="smile outline icon huge green"></i>'
            '</div>'
        )

    # finally, mark the opportunities as not published again
    for o in skipped_opportunities:
        o.fundingopportunity_published = False
        o.save()

    return body
