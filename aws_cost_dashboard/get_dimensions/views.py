from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from calendar import monthrange
from dateutil.relativedelta import relativedelta
import boto3

# global var declaration
client = boto3.client('ce')

# Create your views here.

# this function will return cost for specifies tag within the current month upto today
@api_view(['GET'])
def get_cost_and_usage_for_past_six_months(request):
    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': "start_date_str",
            'End': "end_date_str"
        },
        Granularity='MONTHLY',
        Metrics=[
            'BlendedCost',
            "UnblendedCost",
            "UsageQuantity"
        ],
    )
    return Response(response)


# this function will return cost for specifies tag within the current month upto today
@api_view(['GET'])
def get_cost_and_usage_for_current_month(request):
    start_date = datetime.today().replace(day=1)
    end_date = datetime.today()
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': start_date_str,
            'End': end_date_str
        },
        Granularity='MONTHLY',
        Metrics=[
            'BlendedCost',
            "UnblendedCost",
            "UsageQuantity"
        ],
    )
    return Response(response)

#this method will return all the service dimentions within specified time period
@api_view(['GET'])
def get_dimensions(request):
    response = client.get_dimension_values(
        TimePeriod={
            'Start': '2021-01-10',
            'End': '2021-02-01'
        },
        Dimension='SERVICE'
    )
    return Response(response)


#this method will return all the tags use for cost calculation within specified time perod
@api_view(['GET'])
def get_tags(request):
    one_year_ago = datetime.now() - relativedelta(years=1)
    one_year_ago_str = one_year_ago.strftime('%Y-%m-%d')
    today = datetime.today().date()
    today_str = today.strftime('%Y-%m-%d')
    response = client.get_tags(
        TimePeriod={
            'Start': one_year_ago_str,
            'End': today_str
        }
    )
    return Response(response)

#this method will return cost forecast of the current month
@api_view(['GET'])
def get_forecats_cost(request):
    today = datetime.today().date()
    last_date = today.replace(day=monthrange(today.year, today.month)[1])
    last_date_str = last_date.strftime('%Y-%m-%d')
    today_str = today.strftime('%Y-%m-%d')
    response = client.get_cost_forecast(
        TimePeriod={
            'Start': today_str,
            'End': last_date_str
        },
        Metric='BLENDED_COST',
        Granularity= 'MONTHLY',
    )
    return Response(response)
