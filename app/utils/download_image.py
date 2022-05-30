# Created by: Alex Canales on May 1, 2022

import logging
from urllib.request import urlretrieve


def getListOfPostsThatHaveJPGorPNG(posts):
    listOfPosts = []
    for post in posts:
        logging.info(f'Raw => {post} : {post.url}')
        try:
            if  post.url.endswith('.jpg') or post.url.endswith('.png'):
                listOfPosts.append(post)
        except AttributeError:
            pass        
        
    return listOfPosts



def downloadListOfImagesFromUrl(search, listOfImages):
    for image in listOfImages:
        
        try:
            url = image.url
            fileName = f'app/output/{search}/{image.id}.jpg'
            logging.info(f'Downloading {url} to {fileName}')
            urlretrieve(url, fileName)
        except:
            pass
        