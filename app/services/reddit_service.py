
# Created by: Alex Canales on May 1, 2022
import logging
from asyncio.log import logger
import praw
import os
from dotenv import load_dotenv
load_dotenv()

class Reddit:
    
    def __init__(self):
        self.connection = self.create_reddit_instance()
        self.subreddit = None
        self.user = None
    
    def create_reddit_instance(self):
    
        try:
            connection = praw.Reddit(client_id=os.getenv('CLIENT_ID'),
                                client_secret=os.getenv('CLIENT_SECRET'),
                                username=os.getenv('REDDIT_USERNAME'),
                                password=os.getenv('REDDIT_PASSWORD'),
                                user_agent=os.getenv('REDDIT_USER_AGENT'))
            return connection
        except Exception as err:
            logging.error(err)
            return None


    def getSubreddit(self, subredditName):
        try:
            self.subreddit = self.connection.subreddit(subredditName)
        except Exception as err:
            logging.error(err)
           


    def getUser(self, username):
        
        try:
            self.user = self.connection.redditor(username)
        except Exception as err:
            logging.error(err)


    def getSubredditTopPosts(self, numberOfPosts):
        return self.subreddit.top(limit=numberOfPosts)


    def getSubredditNewPosts(self, numberOfPosts):
        return self.subreddit.new(limit=numberOfPosts)


    def getSubredditHotPosts(self, numberOfPosts):
        return self.subreddit.hot(limit=numberOfPosts)


    def getUserHotPosts(self, numberOfPosts):
        return self.user.hot(limit=numberOfPosts)

    def getUserNewPosts(self, numberOfPosts):
        return self.user.new(limit=numberOfPosts)

    def getUserTopPosts(self, numberOfPosts):
        return self.user.top(limit=numberOfPosts)


    def getImageCollection(self, topic, search, count, popularity):
        images = None
        if topic == 'Subreddit':
            self.getSubreddit(search)
            if popularity == 'Hot':
                images = self.getSubredditHotPosts(count)
            elif popularity == 'New':
                images = self.getSubredditNewPosts(count)
            elif popularity == 'Top':
                images = self.getSubredditTopPosts( count)

        elif topic == 'User':
            self.getUser(search)
            if popularity == 'Hot':
                images = self.getUserHotPosts(count)
            elif popularity == 'New':
                images = self.getUserNewPosts(count)
            elif popularity == 'Top':
                images = self.getUserTopPosts(count)
                            
        return images