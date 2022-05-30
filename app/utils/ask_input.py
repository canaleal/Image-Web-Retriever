def askForSearchInput():
    search = ''
    while search == '':
        search = input('Search: ')
    return search



def askForRedditNumberOfPosts():
    count = 0
    while count == 0:
        try:
            count = int(input('How many posts for Images? '))
        except ValueError:
            print('Please enter a number')
    return count


def askForRedditTopicFromValidArray(validArray):
    topic = ''
    while topic == '':
        topic = input('Topic [Subreddit, User]: ')
        if topic not in validArray:
            print('Please enter a valid option')
            topic = ''
    return topic

def getRedditTopicValueInteger(topic):
    if topic == 'Subreddit':
        return 1
    elif topic == 'User':
        return 2


def askForRedditPopularityFromValidArray(validArray):
    popularity = ''
    while popularity == '':
        popularity = input('Popularity [Hot, New, Top]: ')
        if popularity not in validArray:
            print('Please enter a valid option')
            popularity = ''
    return popularity

def getRedditPopularityValueInteger(popularity):
    if popularity == 'Hot':
        return 1
    elif popularity == 'New':
        return 2
    elif popularity == 'Top':
        return 3