
# Created by: Alex Canales on May 1, 2022

from logging import raiseExceptions
import streamlit as st
from helpers import checkIfFolderExistsAndCreateIfNot, checkInternetConnection, downloadListOfImagesFromUrl, getListOfPostsThatHaveJPGorPNG, downloadListOfImagesFromUrl
from instance import createRedditObject, getSubreddit, getSubredditHotPosts, getSubredditNewPosts, getSubredditTopPosts, getUser, getUserHotPosts, getUserNewPosts, getUserTopPosts
from service import getImageCollection

if __name__ == "__main__":
    try:
        connection = checkInternetConnection()
        checkIfFolderExistsAndCreateIfNot('app/output')
        reddit_object = createRedditObject()
        
        if reddit_object and connection:

            images = None
            search = ''
            count = 0
            topic = ''
            popularity = ''
            
            st.markdown('# Reddit')
            with st.form(key='my_form', clear_on_submit=True):
                search = st.text_input('Search')
                count = st.slider('Check how many posts for Images?', 0, 50, 10)
                topic = st.selectbox('Topic', ['Subreddit', 'User'])
                popularity = st.selectbox('Popularity', ['Hot', 'New', 'Top'])
                submit_button = st.form_submit_button('Get Images')

            if submit_button:
                if search != '' and count != 0 and topic != '' and popularity != '':
                    
                    images = getImageCollection(topic, reddit_object, search, count, popularity) 
                    try:
                        images = getListOfPostsThatHaveJPGorPNG(images)
                        if len(images) > 0:
                            st.success(f'{len(images)} - Images Found!')
                            for image in images:
                                st.image(image.url, width=200)
                                st.write(image.url)
                            
                            
                            downloadListOfImagesFromUrl(search, images)

                        else:
                            st.error('No Images Found!')
                    
                    except ValueError as error:
                        st.error('No Images Found!')
                else:
                    st.error('Please fill all the fields!')
                    
        else:
            raise Exception("Sorry, unable to connect to Reddit!")

    except Exception as err:
        st.error(err)
        

