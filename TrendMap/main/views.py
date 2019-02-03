from django.shortcuts import render, redirect
from django.db import models
from main.models import Tokens

import tweepy
import json

# Create your views here.

def index(request):
    context= {}
    return render(request, 'index.html', context)


def begin_auth(request):
    # token = Tokens.objects.get(id=1)
    # if not token:
    if request.method == 'POST':
        """ Read the secrets file and build the auth object """
        with open('/src/certs/client_secrets.json') as f:
            data = json.load(f)
        consumer_key = data["APIkey"]
        consumer_secret = data["APIkeySecret"]
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

        try:
            redirect_url = auth.get_authorization_url()
            request.session['request_token'] = auth.request_token
        except tweepy.TweepError:
            print('Error! Failed to get request token.')
            return redirect('/')

        return redirect(redirect_url)
    return redirect('/')

def verify(request):
    """ Get the verifier """
    verifier = request.GET.get('oauth_verifier')

    """ Open the secrets file and rebuild the auth object """
    with open('src/certs/client_secrets.json') as f:
        data = json.load(f)
    consumer_key = data["APIkey"]
    consumer_secret = data["APIkeySecret"]
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    token = request.session['request_token']
    del request.session['request_token']
    auth.request_token = {
        'oauth_token': token,
        'oauth_token_secret': verifier
    }
    print(verifier)
    print(token)
    try:
        auth.get_access_token(verifier)
        try:
            token = Tokens.objects.get(id=1)
        except:
            token = Tokens.objects.create(key = auth.access_token, secret = auth.access_token_secret)
            token.save()
    except tweepy.TweepError:
        print('Error! Failed to get access token.')
        return redirect('/')

    return redirect('/')

def get_tweets(request):
    """ Open the secrets file and rebuild the auth object """
    # token = Tokens.objects.get(id=1)
    with open('/src/certs/client_secrets.json') as f:
        data = json.load(f)
    accessToken = data["accessToken"]
    accessTokenSecret = data["accessTokenSecret"]
    consumer_key = data["APIkey"]
    consumer_secret = data["APIkeySecret"]
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(accessToken, accessTokenSecret)



    api = tweepy.API(auth)
    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet)
    context= {
        'public_tweets': public_tweets,
    }
    return render(request, 'index.html', context)
