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
        
    def insert_data(self, name, listOfImages, popularity):
       
        try:
            if self.cursor:
                query = f'INSERT INTO images(name, post_link, post_popularity) VALUES (%s,%s,%s);'
                for image in listOfImages:
                    self.cursor.execute(query, (name, image.url, popularity))
                self.connection.commit()
        except Error as error:
            logging.error(error)
    