import mysql.connector
from mysql.connector import Error

class MySQLDatabase:
    def __init__(self, host, database, user, password):
        self.connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        if self.connection.is_connected():
            print("Connected to MySQL database")

    def insert_ad(self, title, price, availability='In Stock'):
        cursor = self.connection.cursor()
        query = "INSERT INTO ads (title, price, availability) VALUES (%s, %s, %s)"
        cursor.execute(query, (title, price, availability))
        self.connection.commit()
        print("Ad inserted successfully")
        cursor.close()

    def update_ad(self, ad_id, title, price):
        cursor = self.connection.cursor()
        query = "UPDATE ads SET title = %s, price = %s WHERE id = %s"
        cursor.execute(query, (title, price, ad_id))
        self.connection.commit()
        print("Ad updated successfully")
        cursor.close()

    def query_ads(self):
        cursor = self.connection.cursor()
        query = "SELECT * FROM ads"
        cursor.execute(query)
        result = cursor.fetchall()
        for row in result:
            print(row)
        cursor.close()

    def close(self):
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")
