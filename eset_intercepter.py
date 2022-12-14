# Version: 1.0.2 (05.01.2023)
import re
import requests
import time

class EmailConnectError(Exception):
    pass

class Email:
    def __init__(self):
        self.__login = None
        self.__domain = None
        self.__api = 'https://www.1secmail.com/api/v1/'
        
    def register(self):
        url = f'{self.__api}?action=genRandomMailbox&count=1'
        try:
            r = requests.get(url)
        except:
            raise EmailConnectError
        if r.status_code != 200:
            raise EmailConnectError
        self.__login, self.__domain = str(r.content, 'utf-8')[2:-2].split('@')
    
    def login(self, login, domain):
        self.__login = login
        self.__domain = domain
    
    def get_full_login(self):
        return self.__login+'@'+self.__domain
        
    def read_email(self):
        url = f'{self.__api}?action=getMessages&login={self.__login}&domain={self.__domain}'
        try:
            r = requests.get(url)
        except:
            raise EmailConnectError
        if r.status_code != 200:
            raise EmailConnectError
        return r.json()
    
    def get_message(self, message_id):
        url = f'{self.__api}?action=readMessage&login={self.__login}&domain={self.__domain}&id={message_id}'
        try:
            r = requests.get(url)
        except:
            raise EmailConnectError
        if r.status_code != 200:
            raise EmailConnectError
        return r.json()

def eset_intercepter(email_object, delay=1.0):
    while True:
        json = email_object.read_email()
        if json != []:
            message = json[-1]
            if message['from'].find('product.eset.com') != -1:
                message_body = email_object.get_message(message['id'])
                match = re.search(r'token=[a-zA-Z\d:/-]*', message_body['body'])
                if match is not None:
                    token = match.group()[6:]
                    return token
        time.sleep(delay)
