
from app.instance import createRedditObject, getSubreddit, getSubredditHotPosts, getSubredditNewPosts, getSubredditTopPosts, getUser, getUserHotPosts, getUserNewPosts, getUserTopPosts


def test_reddit_instance():
    assert createRedditObject() != None
    
def test_reddit_instance_subreddit():
    reddit = createRedditObject()
    assert getSubreddit(reddit, 'pics') != None
    
def test_reddit_instance_subreddit_hot_posts():
    reddit = createRedditObject()
    subreddit = getSubreddit(reddit, 'pics')
    assert getSubredditHotPosts(subreddit, 1) != None
    
def test_reddit_instance_subreddit_new_posts():
    reddit = createRedditObject()
    subreddit = getSubreddit(reddit, 'pics')
    assert getSubredditNewPosts(subreddit, 1) != None
    
    
def test_reddit_instance_subreddit_top_posts():
    reddit = createRedditObject()
    subreddit = getSubreddit(reddit, 'pics')
    assert getSubredditTopPosts(subreddit, 1) != None
    
def test_reddit_instance_user():
    reddit = createRedditObject()
    assert getUser(reddit, 'pics') != None
    
def test_reddit_instance_user_hot_posts():
    reddit = createRedditObject()
    user = getUser(reddit, 'pics')
    assert getUserHotPosts(user, 1) != None
    

def test_reddit_instance_user_new_posts():
    reddit = createRedditObject()
    user = getUser(reddit, 'pics')
    assert getUserNewPosts(user, 1) != None

    
def test_reddit_instance_user_top_posts():
    reddit = createRedditObject()
    user = getUser(reddit, 'pics')
    assert getUserTopPosts(user, 1) != None