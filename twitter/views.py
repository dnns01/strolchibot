from django.shortcuts import render
from django.http import JsonResponse
import requests
import os


# Create your views here.
def guestbook(request):
    return render(request, "guestbook.html", context={"tweets": get_guestbook_tweets()})


def guestbook_json(request):
    return JsonResponse(get_guestbook_tweets())


def get_guestbook_tweets():
    tweets = {}
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/recent?query=%23StrolchGäBu%20%23StrolchGast&user.fields=name&expansions=author_id&max_results=100&tweet.fields=created_at",
        headers={
            'Authorization': f'Bearer {os.getenv("TWITTER_TOKEN")}'
        })

    response_json = response.json()
    users = {user["id"]: user["name"] for user in response_json["includes"]["users"]}

    for tweet in response_json["data"]:
        tweets[tweet["id"]] = {"author": users[tweet["author_id"]], "text": tweet["text"],
                               "created_at": tweet["created_at"]}

    return tweets