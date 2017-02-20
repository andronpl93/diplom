from django.shortcuts import render
from django.http import HttpResponse
import logging
import json
import csv
import urllib.request
import xml.etree.ElementTree as et
import time

# Create your views here.
def start(request):
    return render(request,'schedule/index.html',{})

def graf(request,par='eur'):
    logging.debug(par)


    return HttpResponse(json.dumps(parseEUR()))




def parseEUR():
    url = [ ['JPY',"http://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/jpy.xml"]]
          # ['USD','http://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/usd.xml']]
          #  ['CAD',"http://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/cad.xml"],
          #  ['AUD',"http://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/aud.xml"],
           # ['QDP',"http://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/gbp.xml"]]
    paket={'dat':[],'len':len(url)}

    for u in range(len(url)):
        tree = []
        urllib.request.install_opener ( urllib.request.build_opener ( urllib.request.ProxyHandler ({ ' HTTP': 'proxy.server: 3128'})))
        tree.append(et.parse(urllib.request.urlopen(url[u][1])))

        root = []
        for i in range(len(tree)):
            root.append(tree[i].getroot())

        a = []
        for i in range(len(root)):
            for j in range(len(root[i])):
                a.append(root[i][j])

        b = []
        for i in range(len(a)):
            for j in range(len(a[i])):
                b.append(a[i][j])


        paket['dat'].append([url[u][0]])
        paket['dat'].append([])
        for i in range(len(b)):
            for j in range(len(b[i])):
                    if b[i][j].get("OBS_VALUE"):
                        paket['dat'][-1].append([])
                        mil=time.mktime(time.strptime(b[i][j].get("TIME_PERIOD"), '%Y-%m-%d'))*1000
                        mil=int(mil)
                        paket['dat'][-1][-1].append(mil)
                        paket['dat'][-1][-1].append(float(b[i][j].get("OBS_VALUE")))


    for i in range(1,len(paket['dat']),2):
        standart=paket['dat'][i][0][-1]
        for j in range(len(paket['dat'][i][:])):
            paket['dat'][i][j][-1]=round(paket['dat'][i][j][-1]/standart,2)

    return paket






logging.basicConfig(
	level = logging.DEBUG,
	format = '%(asctime)s %(levelname)s %(message)s',
)