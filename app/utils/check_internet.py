import requests
from urllib.request import urlretrieve

def checkInternetConnection():
    try:
        requests.get('http://google.com')
        return True
    except:
        return False


def checkIfUrlExists(url):
    try:
        requests.get(url)
        return True
    except:
        return False