import psycopg2
from dotenv import load_dotenv
import os
import time
import argparse
import requests
import hashlib

class cli:
    def __init__(self):
        load_dotenv()
        self.CONNECTION_STRING = os.getenv('DATABASE_URL')
        self.API_KEY = os.getenv('API_KEY')
        
        try:
            self.connection = psycopg2.connect(self.CONNECTION_STRING)
            self.cursor = self.connection.cursor()

        except Exception as error:
            print("drror connecting database:", error)
    
    def hash(self,password):
        sha256_hash = hashlib.sha256()
        sha256_hash.update(password.encode('utf-8'))
        hashed_password = sha256_hash.hexdigest()
        return str(hashed_password)


    def create_user(self, username, password):
        auth = self.authenticate(username,password)
        if auth==(True,False) or auth==True:
            print("username already exists")
            return
        hashed_password = self.hash(password)
        self.cursor.execute(f"INSERT INTO clischema.users (username, password) VALUES (%s, %s)", (username, hashed_password,))
        self.connection.commit()
        print("user created :)")
        return

    def authenticate(self, username, password):
        self.cursor.execute(f"SELECT username, password FROM clischema.users WHERE username = %s", (username,))
        res = self.cursor.fetchone()
        if res:
            hashed_password = self.hash(password)
            if hashed_password==res[1]:
                return True
            else:
                return (True,False)
        else:
            return False

    def search(self, username, password, cityname):
        if self.authenticate(username, password)==(True,False):
            print("wrong password try again")
            return
        if self.authenticate(username, password)==False:
            print("user not exists")
            return
        
        BASE_URL = f'https://api.openweathermap.org/data/2.5/weather?q={cityname}&appid={self.API_KEY}'

        response = requests.get(BASE_URL)
        if response.status_code == 200:
            data = response.json()
            for (i, j) in zip(data.keys(), data.values()):
                print(i, j)
        
        self.cursor.execute(f"INSERT INTO clischema.search_history (username,time_monotonic,search_term) VALUES (%s, %s, %s)", (username, int(time.monotonic()), cityname))
        self.connection.commit()

    def display(self, username, password):
        if self.authenticate(username, password)==(True,False):
            print("wrong password try again")
            return
        if self.authenticate(username, password)==False:
            print("user not exists")
            return
        self.cursor.execute(f"SELECT * FROM clischema.search_history WHERE username = %s", (username,))
        print("id SearchHistory")
        for row in self.cursor.fetchall():
            print(row)
    
    def delete(self, username, password, id):
        if self.authenticate(username, password)==(True,False):
            print("wrong password try again")
            return
        if self.authenticate(username, password)==False:
            print("user not exists")
            return

        self.cursor.execute(f"SELECT username, search_term FROM clischema.search_history WHERE id = %s", (id,))
        res = self.cursor.fetchone()
        self.cursor.execute(f"DELETE FROM clischema.search_history WHERE id = %s", (id,))
        self.connection.commit()
        print(f"search history deleted for username: {res[0]} city: {res[1]}")

    def update(self, username, password, newun):
        if self.authenticate(username, password)==(True,False):
            print("wrong password try again")
            return
        if self.authenticate(username, password)==False:
            print("user not exists")
            return
        
        hashed_password = self.hash(newun)
        self.cursor.execute(f"UPDATE clischema.users SET password= %s WHERE username=%s", (hashed_password, username,))
        self.connection.commit()
        print("password updated successfully :)")

        

def main():
    cl = cli()
    parser = argparse.ArgumentParser(description="A simple CLI tool.")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    search_parser = subparsers.add_parser('search', help="Search")
    search_parser.add_argument('-un', '--username', required=True, help="Username")
    search_parser.add_argument('-ps', '--password', required=True, help="Password")
    search_parser.add_argument('-ct', '--city', required=True, help="City")
    
    create = subparsers.add_parser('create', help="Create User")
    create.add_argument('-un', '--username', required=True, help="Username")
    create.add_argument('-ps', '--password', required=True, help="Password")
    
    update = subparsers.add_parser('update', help="Update Password")
    update.add_argument('-un', '--username', required=True, help="Username")
    update.add_argument('-ps', '--password', required=True, help="Password")
    update.add_argument('-newun', '--newpassword', required=True, help="New Password")
    
    display = subparsers.add_parser('display', help="Display History")
    display.add_argument('-un', '--username', required=True, help="Username")
    display.add_argument('-ps', '--password', required=True, help="Password")

    delete = subparsers.add_parser('delete', help="Display History")
    delete.add_argument('-un', '--username', required=True, help="Username")
    delete.add_argument('-ps', '--password', required=True, help="Password")
    delete.add_argument('-id', '--historyid', required=True, help="History ID")

    args = parser.parse_args()

    if args.command == 'search':
        cl.search(args.username, args.password, args.city)
    if args.command == 'create':
        cl.create_user(args.username, args.password)
    if args.command == 'update':
        cl.update(args.username, args.password, args.newpassword)
    if args.command == 'display':
        cl.display(args.username, args.password)
    if args.command == 'delete':
        cl.delete(args.username, args.password, args.historyid)

if __name__=="__main__":
    main()