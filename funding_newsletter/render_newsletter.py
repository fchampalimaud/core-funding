import sys, os
from django.utils.dateparse import parse_datetime
from funding_opportunities_models.models import FundingOpportunity
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import models
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.timezone import is_aware, make_aware
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


NEW_FUNDS_N_DAYS = 5*30  # show new funding opportunities with
NEW_FUNDS_N_MAX = 6  # Maximum of funds to send
CLOSING_FUNDS_N_DAYS = 30  # number of days required for a fund to be considered a closing fund.
ROLLING_FUNDS_MONTHS = [3, 6, 9]


def next_monday(step=1):
    """Returns next monday as a datetime object.

    Newsletter dissemination is done every monday.
    This is useful to simulate the newsletter in the future.
    `step` is the number of weeks to move further.
    """
    today = timezone.localtime().replace(
        hour=0, minute=0, second=0, microsecond=0)
    return today + timedelta(days=((step*7)-today.weekday()))


# def get_aware_datetime(date_str):
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


def query_new(step=1):
    """New funding opportunities that have not been disseminated"""

    limit_date = next_monday(step) + timedelta(days=NEW_FUNDS_N_DAYS)

    newfunds = FundingOpportunity.objects.filter(
        fundingopportunity_end__gt=next_monday(step),
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


def query_closing(step=1):
    """ Closing in 30 days"""

    limit_date = next_monday(step) + timedelta(days=CLOSING_FUNDS_N_DAYS)

    closingfunds = FundingOpportunity.objects.filter(
        fundingopportunity_end__gt=next_monday(step),
        fundingopportunity_end__lt=limit_date,
        fundingopportunity_end__isnull=False,
    ).order_by(
        'fundingopportunity_end',
        'fundingopportunity_name',
    )
    closingfunds = sorted(
        closingfunds, key=lambda x: x.subject.opportunitysubject_order)

    return closingfunds


# def query_rolling(step=1):
#     """ Rolling Opportunities
#     They should be generated only on the first monday of
#     May, September and January
#     """
#     month = next_monday(step).month

#     if month in ROLLING_FUNDS_MONTHS:
#         first_monday = find_first_monday(next_monday(step).year, month)
#         previous_tuesday = first_monday + timedelta(days=-6)

#         if previous_tuesday <= next_monday(step).date() <= first_monday:
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


def render_newsletter(step=1):

    # Collect opportunities that were disseminated, allegedly...
    skipped_opportunities = []
    for i in range(1, step):
        newfunds = query_new(step)
        skipped_opportunities.extend(newfunds)

    # and mark them as published
    for o in skipped_opportunities:
        o.fundingopportunity_published = True
        o.save()

    # generate the newsletter
    newfunds = query_new(step)
    closingfunds = query_closing(step)
    rollingfunds = []  # query_rolling(step) FIXME !!!!!!!!!!!!!!!!!!!!!

    body = render_to_string(
        'funding_newsletter/funding-opportunities-newsletter.html',
        {
            'newfunds':     newfunds,
            'closingfunds': closingfunds,
            'rollingfunds': rollingfunds,
        }
    )

    # finally, mark the opportunities as not published again
    for o in skipped_opportunities:
        o.fundingopportunity_published = False
        o.save()

    return body
