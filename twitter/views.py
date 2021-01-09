from django.shortcuts import render
from django.http import JsonResponse
import requests


# Create your views here.
def guestbook(request):
    tweets = {}
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/recent?query=%23StrolchGäBu%20%23StrolchGast&user.fields=name&expansions=author_id&max_results=100&tweet.fields=created_at",
        headers={
            'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAADkVLgEAAAAAbQxmw7UXlTMYdcd%2BrcWQ7T8lZlc%3DQjRkgsq3d4XeIXk2vZzagBLuBB5UUlTKwBl8Uz0XafzAfVnAxc'
        })

    response_json = response.json()
    users = {user["id"]: user["name"] for user in response_json["includes"]["users"]}

    for tweet in response_json["data"]:
        print(tweet)
        tweets[tweet["id"]] = {"author" : users[tweet["author_id"]], "text": tweet["text"], "created_at": tweet["created_at"]}

    print(tweets)

    return JsonResponse(tweets)
