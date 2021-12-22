
from django.http.response import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
import requests
import datetime
import matplotlib.pyplot as plt
import os.path
import os
from django.conf import settings

media_root = settings.MEDIA_ROOT
plt.rcParams.update({'font.size': 8})

# Create your views here.
api_key = '9bd530baf9dce72b9e6817b0912f431e'


@api_view(['GET', 'POST'])
def test(request):
    api = f'http://api.openweathermap.org/data/2.5/weather?q=Thane&appid=9bd530baf9dce72b9e6817b0912f431e'
    req = requests.post(url=api)
    print(req.json())
    return HttpResponse(0)


@api_view(['POST'])
def historical(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        print(city)
        lat_api = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=9bd530baf9dce72b9e6817b0912f431e'
        req = requests.post(url=lat_api)
        lat = req.json()['coord']['lat']
        lon = req.json()['coord']['lon']
        day_stamp = datetime.datetime.today() - datetime.timedelta(days=5)
        dt = datetime.datetime.timestamp(day_stamp)
        today = datetime.datetime.timestamp(datetime.datetime.today())
        api = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly&appid={api_key}'
        req_data = requests.post(url=api).json()
        dates = []
        temp = []
        # print(req_data['daily'])
        for i in req_data['daily']:
            dates.append(datetime.datetime.fromtimestamp(i['dt']).strftime("%d/%m/%Y"))
            temp.append(i['temp']['max'])
            print(datetime.datetime.fromtimestamp(i['dt']), i['temp']['max'])
        print(dates, temp)
        total_files = 0
        for base, dirs, files in os.walk('media/graphs/'):
            print('Searching in : ',base)
            for Files in files:
                total_files += 1
        print(total_files)
        filelist = [ f for f in os.listdir('media/graphs/') if f.endswith(".png") ]
        if len(filelist) > 5:
            for f in filelist:
                os.remove(os.path.join('media/graphs/', f))
        plt.figure(clear=True)
        plt.plot(dates, temp,  marker='o')
        plt.margins(x=0.03, y=0.03)
        # plt.legend()
        # plt.subplots_adjust(left=0.1, bottom=0.1, right=0.2, top=0.2)
        plt.xlabel('Dates')
        plt.ylabel('Temperature')
        plt.xticks(rotation=15)
        plt.savefig(f'media/graphs/{city}.png')
        plt.clf()
        # plt.show()
        print(media_root+'media/temp.png')
        url = f'http://127.0.0.1:8000/media/graphs/{city}.png' 
        return Response(url)