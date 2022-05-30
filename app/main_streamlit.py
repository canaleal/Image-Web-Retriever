
# Created by: Alex Canales on May 1, 2022

from logging import raiseExceptions
import streamlit as st

from utils.check_folder import checkIfFolderExistsAndCreateIfNot
from utils.check_internet import checkInternetConnection
from utils.download_image import getListOfPostsThatHaveJPGorPNG, downloadListOfImagesFromUrl
from services.reddit_service import Reddit

if __name__ == "__main__":
    try:
        connection = checkInternetConnection()
        checkIfFolderExistsAndCreateIfNot('app/output')
        reddit_object = Reddit()
        
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
                    
                    images = reddit_object.getImageCollection(topic, search, count, popularity) 
                    try:
                        images = getListOfPostsThatHaveJPGorPNG(images)
                        if len(images) > 0:
                            st.success(f'{len(images)} - Images Found!')
                            for image in images:
                                st.image(image.url, width=200)
                                st.write(image.url)
                            
                         
                            checkIfFolderExistsAndCreateIfNot(f'app/output/{search}')
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
        

