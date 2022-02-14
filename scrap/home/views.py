from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Clone

import requests
from bs4 import BeautifulSoup
import os
from django.conf import settings as django_settings


def index(request):
    return render(request, "index.html")

@csrf_exempt
def create(request):
    if request.method == "POST":
        url = request.POST['url']
        if not url:
            return JsonResponse({'status':'fail', 'message':'Please enter a url to clone.'})

        try:
            r = requests.get(url)
            html = r.content

            soup = BeautifulSoup(html, 'html.parser')
        except:
            return JsonResponse({'status':'fail', 'message':'Some error occured while processing your request.'})

        try:

            links = soup.find_all('link')
            imgs = soup.find_all('img')
            anchors = soup.find_all('a')
            scripts = soup.find_all('script')

            for l in links: 
                try:
                    lhref = l['href']
                except:
                    lhref = None
                if lhref:  
                    if l['href'][0] != 'h':
                        l['href'] = url + l['href']

            for i in imgs:
                try:
                    iscr = i['src']
                except:
                    iscr = None
                if iscr:
                    if i['src'][0] != 'h':
                        i['src'] = url + i['src']

            for a in anchors:
                try:
                    ahref = a['href']
                except:
                    ahref = None
                if ahref:
                    if a['href'][0] != 'h':
                        a['href'] = url + a['href']

            for s in scripts:
                try:
                    src = s['src']
                except:
                    src = None
                if src:
                    if s['src'][0] != 'h':
                        s['src'] = url + s['src']

        except requests.exceptions.ConnectionError:
            return JsonResponse({'status':'fail', 'message':"Connection Timed out."})

        except:
            return JsonResponse({'status':'fail', 'message':'An error occured. Please try any other url.'})

        clone = Clone.objects.create(url = url)

        with open(os.path.join(django_settings.STATIC_ROOT,f"/projects/scrap/scrap/static/clone-{clone.id}.html"), "w", encoding = 'utf-8') as file: 
            file.write(str(soup.prettify()))
        
        clone.save()
        return JsonResponse({'status':'success', 'file':f'clone-{clone.id}.html'})

    else:
        return JsonResponse({'status':'fail', 'message':'Invalid Request'})