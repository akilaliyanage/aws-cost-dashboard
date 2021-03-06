from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from calendar import monthrange
from dateutil.relativedelta import relativedelta
import json
from rest_framework.parsers import JSONParser
from rest_framework import status
import boto3
import requests
import time
from django.db import connection
from random import randrange

# serialzers
from .serializers import TagsSerializer

#models
from .models import Tags

# global var declaration
client = boto3.client('ce',
    aws_access_key_id='AKIAZ67XFEUH74LDRDTX',
    aws_secret_access_key='QVf9h7flXvPtUf5VJlK63H0A6PLVp2fqIEIYs7Hv')

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
            'BlendedCost'
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
            'BlendedCost'
        ],
    )
    return Response(response)


# this method will return all the service dimentions within specified time perio
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


# this method will return all the tags use for cost calculation within specified time perod
@api_view(['GET'])
def get_tags(request):
    one_year_ago = datetime.now() - relativedelta(years=1)
    one_year_ago_str = one_year_ago.strftime('%Y-%m-%d')
    today = datetime.today().date()
    today_str = today.strftime('%Y-%m-%d')

    cursor = connection.cursor()
    cursor.execute("truncate table aws.get_dimensions_tags;")

    response = client.get_tags(
        TimePeriod={
            'Start': one_year_ago_str,
            'End': today_str
        },
        TagKey='Name',  #chnage this to take values for the defind key
    )
    res_json = json.dumps(response)
    data = {}
    jsonObject = json.loads(res_json)
    for Tags in jsonObject['Tags']:
        if(Tags == ''):
            continue
        else:
            cursor.execute("insert into aws.get_dimensions_tags values('{0}', '{1}', '{2}');".format(int(randrange(1, 9999999999)),'role',str(Tags)))

    return JsonResponse(status=status.HTTP_201_CREATED)

# this method will return cost forecast of the current month


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
        Granularity='MONTHLY',
    )
    return Response(response)


@api_view(['POST'])
# test db create method
def save_to_db(request):
    data = JSONParser().parse(request)
    tag_serializer = TagsSerializer(data=data)

    if tag_serializer.is_valid():
        tag_serializer.save()
        return JsonResponse(tag_serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(tag_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def db_get_all_tags(request):
    tags = Tags.objects.all()
    tag_serializer = TagsSerializer(tags, many=True)
    return Response(tag_serializer.data)
