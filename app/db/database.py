import logging
from msilib import schema
import psycopg2
from psycopg2 import Error
import os
from dotenv import load_dotenv
load_dotenv()


class Database:
    
    def __init__(self):
        self.connection = self.create_postgres_database_connection()
        self.cursor = self.create_cursor_if_connection_is_open()
        
    def create_postgres_database_connection(self):
        try:
            connection = psycopg2.connect(user=os.getenv('DB_USER'),
                                          password=os.getenv('DB_PASSWORD'),
                                          host=os.getenv('DB_HOST'),
                                          port=os.getenv('DB_PORT'),
                                          database=os.getenv('DB_NAME'))
            return connection
        except Error as error:
            logging.error(error)
            
    def ping_database(self):
        try:
            if self.connection:
                self.connection.ping()
        except Error as error:
            logging.error(error)

    def create_cursor_if_connection_is_open(self):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                return cursor
        except Error as error:
            logging.error(error)
        
    def close_connection_if_open(self):
        try:
            if self.connection:
                self.connection.close()
        except Error as error:
            logging.error(error)
       
        
    def close_cursor_if_open(self):
        try:
            if self.cursor:
                self.cursor.close()
        except Error as error:
            logging.error(error)
            
    def close_database(self):
        self.close_connection_if_open()
        self.close_cursor_if_open()
        
    def get_bool_if_value_in_column_exists(self, table, column, value):
        try:
            if self.cursor:
                query = f'SELECT EXISTS(SELECT 1 FROM {table} WHERE {column} = %s);'
                self.cursor.execute(query, (value,))
                return self.cursor.fetchone()[0]
        except Error as error:
            logging.error(error)
        
    def insert_reddit_image_data(self, name, topic, popularity, listOfImages):
       
        try:
            if self.cursor:
                query = f'INSERT INTO reddit_images(name, topic, post_popularity, post_link, post_title) VALUES (%s,%s,%s,%s,%s);'
                for image in listOfImages:
                    self.cursor.execute(query, (name, topic, popularity, image.url, image.title) )
                self.connection.commit()
        except Error as error:
            logging.error(error)
    
    def insert_general_image_data(self, listOfImages):    
        try:
            
            exists = self.get_bool_if_value_in_column_exists('general_images', 'name', listOfImages[0].name)
            
            if self.cursor and not exists:
                query = f'INSERT INTO general_images(name, container_link, image_link) VALUES (%s,%s,%s);'
                for generalImage in listOfImages:
                    self.cursor.execute(query, (generalImage.name, generalImage.container_link, generalImage.image_link) )
                self.connection.commit()
            else:
                logging.error('Image already exists in database')
                
        except Error as error:
            logging.error(error)