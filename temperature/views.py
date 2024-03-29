# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from darksky import get_url, make_api_call

# Create your views here.
@csrf_exempt
def home(request):
    return render(request, "temperature/home.htm")


@csrf_exempt
def post_temperature(request):
    regex = re.compile(r'^([\-]?[\d]{1,2}[\.]{1}[\d]{1,4})|([\-]?[\d]{1,2})$')
    errors = []
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        if not latitude or not longitude:
            errors.append('Latitude and longitude fields cannot be blank. Please type a valid value.')
        elif regex.match(latitude) and regex.match(longitude):
            post_url = get_url(latitude, longitude)
            celsius = make_api_call(post_url)
            msg = "Temperature at: {}, {} is {}ºC".format(latitude, longitude, celsius)
            return render(request, 'temperature/home.htm', {
                "lat": latitude,
                "long": longitude,
                "celsius": celsius,
                "temperature_msg": msg
            })
        else:
            errors.append('Please type valid values. Examples: "23.454", "12", "-12.342"')
        return render(request, 'temperature/home.htm', {'errors': errors})
