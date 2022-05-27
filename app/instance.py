
# Created by: Alex Canales on May 1, 2022

import praw
import os
from dotenv import load_dotenv
load_dotenv()

    
def createRedditObject():
   
    try:
        reddit = praw.Reddit(client_id=os.getenv('CLIENT_ID'),
                            client_secret=os.getenv('CLIENT_SECRET'),
                            username=os.getenv('REDDIT_USERNAME'),
                            password=os.getenv('REDDIT_PASSWORD'),
                            user_agent=os.getenv('REDDIT_USER_AGENT'))
        return reddit
    except Exception as err:
        return None


def getSubreddit(reddit, subredditName):
    subreddit = reddit.subreddit(subredditName)
    return subreddit


def getUser(reddit, username):
    return reddit.redditor(username)


def getSubredditTopPosts(subreddit, numberOfPosts):
    return subreddit.top(limit=numberOfPosts)


def getSubredditNewPosts(subreddit, numberOfPosts):
    return subreddit.new(limit=numberOfPosts)


def getSubredditHotPosts(subreddit, numberOfPosts):
    return subreddit.hot(limit=numberOfPosts)


def getUserHotPosts(user, numberOfPosts):
    return user.hot(limit=numberOfPosts)

def getUserNewPosts(user, numberOfPosts):
    return user.new(limit=numberOfPosts)

def getUserTopPosts(user, numberOfPosts):
    return user.top(limit=numberOfPosts)


def getImageCollection(topic, reddit_object, search, count, popularity):
    images = None
    if topic == 'Subreddit':
        subreddit = getSubreddit(reddit_object, search)
        if popularity == 'Hot':
            images = getSubredditHotPosts(subreddit, count)
        elif popularity == 'New':
            images = getSubredditNewPosts(subreddit, count)
        elif popularity == 'Top':
            images = getSubredditTopPosts(subreddit, count)

    elif topic == 'User':
        user = getUser(reddit_object, search)
        if popularity == 'Hot':
            images = getUserHotPosts(user, count)
        elif popularity == 'New':
            images = getUserNewPosts(user, count)
        elif popularity == 'Top':
            images = getUserTopPosts(user, count)
                        
    return images