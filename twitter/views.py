from django.shortcuts import render
from django.http import JsonResponse
import requests
import os


# Create your views here.
def guestbook(request):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/recent?query=%23StrolchGäBu%20%23StrolchGast&max_results=100",
        headers={
            'Authorization': f'Bearer {os.getenv("TWITTER_TOKEN")}'
        })

    response_json = response.json()
    return JsonResponse([tweet["id"] for tweet in response_json["data"]], safe=False)


def jojo(request):
    response = requests.get(
        "https://api.twitter.com/2/users/1279020408050761730/tweets?max_results=100",
        headers={
            'Authorization': f'Bearer {os.getenv("TWITTER_TOKEN")}'
        })

    response_json = response.json()
    return JsonResponse(response_json)



