
from instance import createRedditObject, getSubreddit, getSubredditHotPosts, getSubredditNewPosts, getSubredditTopPosts, getUser, getUserHotPosts, getUserNewPosts, getUserTopPosts


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